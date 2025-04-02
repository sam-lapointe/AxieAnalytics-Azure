import azure.functions as func
import logging
import os
import hmac
import hashlib
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.servicebus import ServiceBusClient, ServiceBusMessage


# Constants and environment variables
KEY_VAULT_NAME = os.environ["KEY_VAULT_NAME"]
SECRET_SIGNING_KEY = os.environ["SIGNING_KEY"]
AUTHORIZED_IPS = os.environ["AUTHORIZED_IPS"].split(',')
KEY_VAULT_URL = f"https://{KEY_VAULT_NAME}.vault.azure.net"
FULLY_QUALIFIED_NAMESPACE = os.environ["SERVICEBUS_FULLY_QUALIFIED_NAMESPACE"]
TOPIC_NAME = os.environ["SERVICEBUS_TOPIC_NAME"]

# Authenticate to Azure
credential = DefaultAzureCredential()
key_vault_client = SecretClient(KEY_VAULT_URL, credential)
servicebus_client = ServiceBusClient(FULLY_QUALIFIED_NAMESPACE, credential, logging_enable=True)

# Alchemy signing key to validate the signature
SIGNING_KEY = key_vault_client.get_secret(SECRET_SIGNING_KEY).value

# Application initialization
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# Helper function to validate the signature
def is_valid_signature_for_string_body(body: str, signature: str, signing_key: str) -> bool:
    digest = hmac.new(
        bytes(signing_key, "utf-8"),
        msg = body,
        digestmod = hashlib.sha256,
    ).hexdigest()

    return signature == digest


# Helper function to send message to Azure Service Bus
def send_single_message(sender, message):
    message = ServiceBusMessage(message)
    sender.send_messages(message)


@app.route(route="webhook")
def AlchemyWebhook(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    source_ip = req.headers.get('x-forwarded-for')
    # Verifies if the request if coming from an authorized IP address
    if source_ip not in AUTHORIZED_IPS:
        logging.error(f"Request coming from unauthorized IP address: {source_ip}")
        return func.HttpResponse(status_code=403)

    signature = req.headers.get('x-alchemy-signature')
    # Verify if the Alchemy signature is in the header
    if not signature:
        logging.error("Missing signature in headers.")
        return func.HttpResponse(status_code=400)

    # Get the body content
    try:
        req_body = req.get_json()
        logging.info(f"Body Size: {len(bytes(str(req_body), 'utf-8'))} bytes")
    except ValueError:
        logging.error("Missing body.")
        return func.HttpResponse(status_code=400)
    except Exception as e:
        logging.error(f"Unknown error with the request body: {e}")
        return func.HttpResponse(status_code=400)
    
    # Verify if the signature is valid
    if not is_valid_signature_for_string_body(req.get_body(), signature, SIGNING_KEY):
        logging.error("The signature is invalid.")
        return func.HttpResponse(status_code=401)
    
    # Verify is there is a body to the request
    if not req_body:
        logging.error("Missing body.")
        return func.HttpResponse(status_code=400)
    
    # Loop throuh reveived transactions and send a message to Azure Service Bus Topic for every transaction
    try:
        logs = req_body["event"]["data"]["block"]["logs"]
        transactions = set()
        for log in logs:
            transaction = log["transaction"]["hash"]
            if transaction in transactions:
                logging.info(f"Transaction {transaction} has already been sent.")
            else:
                transactions.add(transaction)
                message = {
                    "blockNumber": req_body["event"]["data"]["block"]["number"],
                    "transactionHash": transaction
                }
                with servicebus_client:
                    sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
                    with sender:
                        send_single_message(sender, str(message))
                logging.info(f"Transaction {transaction} has been sent.")
    except KeyError as k:
        logging.critical(f"Error while creating the message: Key {k} doesn't exist.")
        return func.HttpResponse(status_code=500)
    except Exception as e:
        logging.critical(f"Unknown error while creating or sending the message: {e}")
        return func.HttpResponse(status_code=500)

    return func.HttpResponse(status_code=200)