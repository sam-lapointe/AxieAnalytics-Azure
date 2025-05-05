import azure.functions as func
import logging
import os
import ast
import asyncpg
from transaction import Transaction
from store_sales import StoreSales
from urllib.parse import quote_plus
from azure.keyvault.secrets.aio import SecretClient
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
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
    def get_servicebus_topic_sales_name() -> str:
        topic_sales_name = os.getenv("SERVICEBUS_TOPIC_SALES_NAME")
        if not topic_sales_name:
            logging.critical("SERVICEBUS_TOPIC_SALES_NAME is not set.")
            raise ValueError(
                "SERVICEBUS_TOPIC_SALES_NAME environment variable is required."
            )
        return topic_sales_name

    @staticmethod
    def get_servicebus_topic_axies_name() -> str:
        topic_axies_name = os.getenv("SERVICEBUS_TOPIC_AXIES_NAME")
        if not topic_axies_name:
            logging.critical("SERVICEBUS_TOPIC_AXIES_NAME is not set.")
            raise ValueError(
                "SERVICEBUS_TOPIC_AXIES_NAME environment variable is required."
            )
        return topic_axies_name

    @staticmethod
    def get_servicebus_topic_sales_subscription_name() -> str:
        subscription_name = os.getenv("SERVICEBUS_SALES_SUBSCRIPTION_NAME")
        if not subscription_name:
            logging.critical("SERVICEBUS_SALES_SUBSCRIPTION_NAME is not set.")
            raise ValueError(
                "SERVICEBUS_SALES_SUBSCRIPTION_NAME environment variable is required."
            )
        return subscription_name

    @staticmethod
    async def get_pg_connection_string(key_vault_client: SecretClient) -> str:
        try:
            # Retrieve environment variables.
            kv_pg_username = os.getenv("KV_PG_USERNAME")
            kv_pg_password = os.getenv("KV_PG_PASSWORD")
            pg_host = os.getenv("PG_HOST")
            pg_port = os.getenv("PG_PORT")
            pg_database = os.getenv("PG_DATABASE")

            # Validate required environment variables.
            if not kv_pg_username:
                logging.critical("KV_PG_USERNAME is not set.")
                raise ValueError("KV_PG_USERNAME environment variable is required.")
            if not kv_pg_password:
                logging.critical("KV_PG_PASSWORD is not set.")
                raise ValueError("KV_PG_PASSWORD environment variable is required.")
            if not pg_host:
                logging.critical("PG_HOST is not set.")
                raise ValueError("PG_HOST environment variable is required.")
            if not pg_port:
                logging.critical("PG_PORT is not set.")
                raise ValueError("PG_PORT environment variable is required.")
            if not pg_database:
                logging.critical("PG_DATABASE is not set.")
                raise ValueError("PG_DATABASE environment variable is required.")

            # Retrieves the PostgreSQL Credentials from Key Vault and URL encodes them.
            pg_username_secret = await key_vault_client.get_secret(kv_pg_username)
            pg_password_secret = await key_vault_client.get_secret(kv_pg_password)
            pg_username = quote_plus(pg_username_secret.value)
            pg_password = quote_plus(pg_password_secret.value)

            connection_string = f"postgres://{pg_username}:{pg_password}@{pg_host}.postgres.database.azure.com:{pg_port}/{pg_database}"
            return connection_string

        except Exception as e:
            logging.error(f"Error constructing PostgreSQL connection string: {e}")
            raise e

    # Validate required environment variables
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
servicebus_topic_sales_subscription_name = (
    Config.get_servicebus_topic_sales_subscription_name()
)
servicebus_topic_sales_name = Config.get_servicebus_topic_sales_name()

app = func.FunctionApp()


@app.service_bus_topic_trigger(
    arg_name="azservicebus",
    subscription_name=servicebus_topic_sales_subscription_name,
    topic_name=servicebus_topic_sales_name,
    connection="ServiceBusConnection",
)
async def store_axie_sales(azservicebus: func.ServiceBusMessage):
    message_body = ast.literal_eval(azservicebus.get_body().decode("utf-8"))
    logging.info(
        "Python ServiceBus Topic trigger processed a message: %s", message_body
    )

    transaction_hash = message_body["transactionHash"]
    block_number = message_body["blockNumber"]
    block_timestamp = message_body["blockTimestamp"]

    # Initialize dependencies
    conn = await asyncpg.connect(
        dsn=await Config.get_pg_connection_string(key_vault_client), ssl="require"
    )  # PostgreSQL connection
    w3 = AsyncWeb3(
        AsyncWeb3.AsyncHTTPProvider(Config.get_node_provider())
    )  # Ronin Node provider

    # Call Transaction class to get the sales list from a transaction hash.
    sales_list = await Transaction(conn, w3).process_logs(transaction_hash)

    # Call the StoreSales class to store the sales in the database and send message to the axies topic.
    async with ServiceBusClient(
        Config.get_servicebus_full_namespace(), credential, logging_enable=True
    ) as servicebus_client:
        axies_topic_name = Config.get_servicebus_topic_axies_name()

        await StoreSales(
            conn,
            servicebus_client,
            axies_topic_name,
            sales_list,
            block_number,
            block_timestamp,
            transaction_hash,
        ).add_to_db()

    logging.info(
        f"All sales of transaction {transaction_hash} have been added successfuly to the database and messages have been sent to the axies topic."
    )
