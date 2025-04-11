import hmac
import hashlib
import json
import pytest
from azure.functions import HttpRequest
from function_app import AlchemyWebhook

@pytest.fixture
def mock_config(mocker):
    mocker.patch("function_app.Config.get_key_vault_url", return_value="https://mock.vault.azure.net")
    mocker.patch("function_app.Config.get_signing_key_name", return_value="mock_signing_key")
    mocker.patch("function_app.Config.get_authorized_ips", return_value=["192.168.0.12", "192.168.0.13"])
    mocker.patch("function_app.Config.get_servicebus_full_namespace", return_value="https://mock-namespace.servicebus.windows.net")
    mocker.patch("function_app.Config.get_servicebus_topic_name", return_value="mock_topic")

@pytest.fixture
def mock_credential(mocker):
    mocker.patch("function_app.DefaultAzureCredential")

@pytest.fixture
def mock_key_vault_client(mocker):
    mocker.patch("function_app.SecretClient")

@pytest.fixture
def mock_servicebus(mocker):
    mock_servicebus_client = mocker.patch("function_app.ServiceBusClient")

    mock_client_instance = mocker.MagicMock()
    mock_servicebus_client.return_value.__aenter__.return_value = mock_client_instance

    mock_sender = mocker.MagicMock()
    mock_sender.send_messages = mocker.AsyncMock()
    mock_client_instance.get_topic_sender.return_value.__aenter__.return_value = mock_sender

@pytest.fixture
def valid_ip():
    return "192.168.0.12"

@pytest.fixture
def valid_request_body():
    return {'webhookId': 'wh_kpy9f3j05p4b3hh8', 'id': 'whevt_fjlzk3zu8uq1p0q1', 'createdAt': '2025-04-10T19:20:21.997Z', 'type': 'GRAPHQL', 'event': {'data': {'block': {'hash': '0xf95b5c3227fc15c4c882f8287b490b99e629dc31dd015da2b7a9d6d4b0ee0f93', 'number': 44153279, 'timestamp': 1744312821, 'logs': [{'topics': ['0x968d1942d9971cb9c45c722957d854c38f327206399d12ae49ca2f9c5dd06fda'], 'account': {'address': '0xfff9ce5f71ca6178d3beecedb61e7eff1602950e'}, 'transaction': {'hash': '0xb05e64ab435371a5c4b6e23f416a37fec881419228db0e35d9b3549204f549eb'}}]}}, 'sequenceNumber': '10000000000632266001', 'network': 'RONIN_MAINNET'}}

@pytest.fixture
def signing_key():
    return "abcdef_f4536"

@pytest.fixture
def mock_get_signing_key(mocker, signing_key):
    mocker.patch("function_app.get_signing_key", return_value=signing_key)

@pytest.fixture(autouse=True)
def mock_dependencies(mock_config, mock_credential, mock_key_vault_client, mock_get_signing_key, mock_servicebus):
    pass

@pytest.fixture
def valid_signature(valid_request_body, signing_key):
    signature = hmac.new(
        bytes(signing_key, "utf-8"),
        msg = bytes(json.dumps(valid_request_body, separators=(',', ':')), "utf-8"),
        digestmod = hashlib.sha256,
    ).hexdigest()

    return signature

@pytest.fixture
def valid_request_headers(valid_signature, valid_ip):
    return {
        "x-alchemy-signature": valid_signature,
        "x-forwarded-for": valid_ip
    }

@pytest.fixture(autouse=True)
def create_request():
    def _create_request(body, headers):
        return HttpRequest(
            method="POST",
            url="/webhook",
            headers=headers,
            body=bytes(json.dumps(body, separators=(',', ':')), "utf-8")
        )
    return _create_request


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "signature, expected_status",
    [
        ("valid_sig", 200),
        ("19d6dd36cb0e7a4a25a9bb841494ee666d60099bf787149c6088cfab6989cd67", 401),
        (None, 400)
    ]
)
async def test_signature(create_request, valid_request_body, valid_ip, valid_signature, signature, expected_status, mock_dependencies):
    headers = {
        "x-forwarded-for": valid_ip,
    }

    if signature == "valid_sig":
        headers["x-alchemy-signature"] = valid_signature
    elif signature is not None:
        headers["x-alchemy-signature"] = signature

    req = create_request(valid_request_body, headers)

    response = await AlchemyWebhook(req)
    assert response.status_code == expected_status

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip_address, expected_status",
    [
        ("192.168.0.12", 200),
        ("192.168.0.13", 200),
        ("192.168.0.16", 403),
        ("10.15.205.104", 403),
        (None, 403)
    ]
)
async def test_allow_authorized_ips(create_request, valid_request_body, valid_signature, ip_address, expected_status, mock_dependencies):
    headers = {
        "x-alchemy-signature": valid_signature
    }

    if ip_address is not None:
        headers["x-forwarded-for"] = ip_address

    req = create_request(valid_request_body, headers)

    response = await AlchemyWebhook(req)
    assert response.status_code == expected_status


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ip_address, expected_status",
    [
        ("192.168.0.12", 200),
        ("192.168.0.13", 200),
        ("192.168.0.16", 200),
        ("10.15.205.104", 200),
        (None, 200)
    ]
)
async def test_allow_all_ips(mocker, create_request, valid_request_body, valid_signature, ip_address, expected_status, mock_dependencies):
    mocker.patch("function_app.Config.get_authorized_ips", return_value=[])

    headers = {
        "x-alchemy-signature": valid_signature
    }

    if ip_address is not None:
        headers["x-forwarded-for"] = ip_address

    req = create_request(valid_request_body, headers)

    response = await AlchemyWebhook(req)
    assert response.status_code == expected_status