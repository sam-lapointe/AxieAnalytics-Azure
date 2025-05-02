import azure.functions as func
import logging
import os
import ast
import aiohttp
import asyncpg
from transaction import Transaction
from store_sales import StoreSales
from azure.keyvault.secrets.aio import SecretClient
from azure.identity.aio import DefaultAzureCredential
from web3 import AsyncWeb3


class Config:
    @staticmethod
    def get_key_vault_url() -> str:
        key_vault_name = os.getenv("KEY_VAULT_NAME")
        if not key_vault_name:
            logging.critical("KEY_VAULT_NAME is not set.")
            raise ValueError("KEY_VAULT_NAME environment variable is required.")
        return f"https://{key_vault_name}.vault.azure.net"

    @staticmethod
    def get_servicebus_full_namespace() -> str:
        full_namespace = os.getenv("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE")
        if not full_namespace:
            logging.critical("SERVICEBUS_FULLY_QUALIFIED_NAMESPACE is not set.")
            raise ValueError(
                "SERVICEBUS_FULLY_QUALIFIED_NAMESPACE environment variable is required."
            )
        return full_namespace

    @staticmethod
    def get_servicebus_topic_name() -> str:
        topic_name = os.getenv("SERVICEBUS_TOPIC_NAME")
        if not topic_name:
            logging.critical("SERVICEBUS_TOPIC_NAME is not set.")
            raise ValueError("SERVICEBUS_TOPIC_NAME environment variable is required.")
        return topic_name
    
    @staticmethod
    def get_servicebus_topic_subscription_name() -> str:
        subscription_name = os.getenv("SERVICEBUS_TOPIC_SUBSCRIPTION_NAME")
        if not subscription_name:
            logging.critical("SERVICEBUS_TOPIC_SUBSCRIPTION_NAME is not set.")
            raise ValueError("SERVICEBUS_TOPIC_SUBSCRIPTION_NAME environment variable is required.")
        return subscription_name
    
    @staticmethod
    def get_pg_connection_string(key_vault_client: SecretClient) -> str:
        pg_connection_string = os.getenv("PG_CONNECTION_STRING")
        if not pg_connection_string:
            logging.critical("PG_CONNECTION_STRING is not set.")
            raise ValueError("PG_CONNECTION_STRING environment variable is required.")
        return pg_connection_string
    
    @staticmethod
    def get_node_provider() -> str:
        node_provider_url = os.getenv("NODE_PROVIDER")
        if not node_provider_url:
            logging.critical("NODE_PROVIDER is not set.")
            raise ValueError("NODE_PROVIDER environment variable is required.")
        return node_provider_url


# Authenticate to Azure
credential = DefaultAzureCredential()
key_vault_client = SecretClient(Config.get_key_vault_url(), credential)

# Servicebus Variables
servicebus_topic_subscription_name = Config.get_servicebus_topic_subscription_name()
servicebus_topic_name = Config.get_servicebus_topic_name()


app = func.FunctionApp()

@app.service_bus_topic_trigger(arg_name="azservicebus", subscription_name=servicebus_topic_subscription_name,
                               topic_name=servicebus_topic_name, connection="ServiceBusConnection") 
async def store_axie_sales(azservicebus: func.ServiceBusMessage):
    message_body = ast.literal_eval(azservicebus.get_body().decode('utf-8'))
    logging.info('Python ServiceBus Topic trigger processed a message: %s', message_body)

    transaction_hash = message_body["transactionHash"]
    block_number = message_body["blockNumber"]
    block_timestamp = message_body["blockTimestamp"]

    # Initialize dependencies
    conn = await asyncpg.connect(dsn=Config.get_pg_connection_string, ssl="require")  # PostgreSQL connection
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(Config.get_node_provider))  # Ronin Node provider

    # Call Transaction class to get the sales list from a transaction hash.
    async with aiohttp.ClientSession() as http_client:
        transaction = Transaction(conn, w3, http_client)
        sales_list = transaction.process_logs(transaction_hash)

    # TODO: Call the StoreSales class to store the sales in the database
    store_sales = StoreSales(conn, sales_list, block_number, block_timestamp)
