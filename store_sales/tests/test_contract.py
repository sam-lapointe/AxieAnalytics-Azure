import pytest
import sys
import asyncpg
import aiohttp
from pathlib import Path
from web3 import Web3

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
print(sys.path)
from contract import (
    datetime,
    timezone,
    Contract,
    ContractNotFoundError,
    EventNotFoundError,
    RecursionError,
)

@pytest.fixture
def conn(mocker):
    return mocker.AsyncMock()

@pytest.fixture
def w3(mocker):
    return mocker.AsyncMock()


@pytest.mark.parametrize(
    "contract_address, visited_addresses",
    [
        ('0x1234567890abcdef1234567890abcdef12345678', None),
        ('0xabcdefabcdefabcdefabcdefabcdefabcdefabcd', set('0x1234567890abcdef1234567890abcdef12345678')),
        ('0xabcdefabcdefabcdefabcdefabcdefabcdefabcd', set('0xabcdefabcdefabcdefabcdefabcdefabcdefabcd')),
    ]
)
@pytest.mark.asyncio
async def test_create(mocker, conn, w3, contract_address, visited_addresses):
    mocker.patch("contract.Contract._Contract__get_contract_data", return_value=None)

    if visited_addresses == contract_address:
        with pytest.raises(RecursionError):
            Contract.create(conn, w3, contract_address, visited_addresses)
    elif visited_addresses is None:
        contract = await Contract.create(conn, w3, contract_address, visited_addresses)
        assert contract is not None
        assert isinstance(contract, Contract)

@pytest.mark.asyncio
async def test_get_contract_data_exists_in_db(mocker, conn, w3):
    # Mock the database fetchrow method to return the proxy and implementation contract data
    conn.fetchrow.side_effect = [
        {
            "contract_name": "ProxyContract",
            "is_proxy": True,
            "abi": "[]",
            "implementation_address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        },
        {
            "contract_name": "ImplementationContract",
            "is_proxy": False,
            "abi": "[]",
            "implementation_address": None,
        }
    ]

    # Create contract instance
    contract = await Contract.create(conn, w3, '0x1234567890abcdef1234567890abcdef12345678', None)

    assert contract._Contract__name == "ProxyContract"
    assert contract._Contract__is_proxy == True
    assert contract._Contract__abi == []
    assert contract._Contract__contract_address == Web3.to_checksum_address('0x1234567890abcdef1234567890abcdef12345678')
    assert isinstance(contract._Contract__implementation, Contract)
    assert contract._Contract__implementation._Contract__name == "ImplementationContract"
    assert contract._Contract__implementation._Contract__is_proxy == False
    assert contract._Contract__implementation._Contract__abi == []
    assert contract._Contract__implementation._Contract__implementation == None
    assert contract._Contract__implementation._Contract__contract_address == Web3.to_checksum_address('0xabcdefabcdefabcdefabcdefabcdefabcdefabcd')

@pytest.mark.asyncio
async def test_get_contract_data_not_in_db(mocker, conn, w3):
    # Mock database fetchrow to return None initially
    conn.fetchrow.side_effect = [None, {
        "contract_name": "TestContract",
        "is_proxy": False,
        "abi": "[]",
        "implementation_address": None,
    }]

    # Mock __add_contract_data
    mocker.patch.object(Contract, "_Contract__add_contract_data", new_callable=mocker.AsyncMock)

    # Create contract instance
    contract = await Contract.create(conn, w3, '0x1234567890abcdef1234567890abcdef12345678', None)

    assert contract._Contract__name == "TestContract"
    assert contract._Contract__is_proxy == False
    assert contract._Contract__abi == []
    assert contract._Contract__implementation == None
    assert contract._Contract__contract_address == Web3.to_checksum_address('0x1234567890abcdef1234567890abcdef12345678')

    contract._Contract__add_contract_data.assert_called_once()
    assert conn.fetchrow.call_count == 2

@pytest.mark.asyncio
async def test_get_contract_data_missing_after_add(mocker, conn, w3):
    # Mock database fetchrow to return None two times
    conn.fetchrow.side_effect = [None, None]

    # Mock __add_contract_data
    mocker.patch.object(Contract, "_Contract__add_contract_data", new_callable=mocker.AsyncMock)

    # Create contract instance
    with pytest.raises(ContractNotFoundError):
        contract = await Contract.create(conn, w3, '0x1234567890abcdef1234567890abcdef12345678', None)
        contract._Contract__add_contract_data.assert_called_once()

    assert conn.fetchrow.call_count == 2

# TODO Test __add_contract_data for fetching and storing contract
@pytest.mark.asyncio
async def test_add_contract_data(mocker, conn, w3):
    # Mock the current time
    mock_current_time = datetime(2025, 5, 9, 12, 0, 0, tzinfo=timezone.utc)
    mock_datetime = mocker.patch("contract.datetime")
    mock_datetime.now.return_value = mock_current_time

    # Mock HTTP session and responses
    mock_http_session = mocker.patch("aiohttp.ClientSession")
    mock_http_client_instance = mock_http_session.return_value
    mock_http_client_instance.__aenter__.return_value = mock_http_client_instance
    mock_http_client_instance.__aexit__.return_value = None

    mock_abi_response = mocker.AsyncMock()
    mock_abi_response.__aenter__.return_value.json.return_value = {
        "result": {
            "output": {
                "abi": []
            }
        }
    }

    mock_contract_response = mocker.AsyncMock()
    mock_contract_response.__aenter__.return_value.json.return_value = {
        "result": {
            "contract": {
                "verifiedName": "TestContract",
            }
        }
    }

    mock_http_client_instance.__aenter__.return_value.get.side_effect = [
        mock_abi_response,
        mock_contract_response,
    ]

    # Mock get_storage_at to return a valid bytes object
    w3.eth.get_storage_at = mocker.AsyncMock(return_value=bytes.fromhex("000000000000000000000000abcdefabcdefabcdefabcdefabcdefabcdefabcd"))

    contract = Contract(conn, w3, '0x1234567890abcdef1234567890abcdef12345678')
    await contract._Contract__add_contract_data()

    contract_data = {
        "contract_address": contract._Contract__contract_address,
        "contract_name": "TestContract",
        "abi": "[]",
        "is_contract_proxy": True,
        "implementation_address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd",
        "created_at": mock_current_time,
        "modified_at": mock_current_time,
    }

    # The indentation of the query string is important to match the expected format
    conn.execute.assert_called_once_with(
                    """
                    INSERT INTO contracts(
                        contract_address,
                        contract_name,
                        abi,
                        is_proxy,
                        implementation_address,
                        created_at,
                        modified_at                      
                    )
                    VALUES (
                        $1, $2, $3, $4, $5, $6, $7
                    )
                    """,
        *contract_data.values(),
    )

# TODO Test __add_contract_data for UniqueViolationError


# TODO Test get_contract_address


# TODO Test get_event_name


# TODO Test get_event_data


# TODO Test get_event_signature_hash


# TODO Test get_event_signature_hash for EventNotFoundError