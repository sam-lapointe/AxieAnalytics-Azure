import azure.functions as func
import logging
import os
import ast
import asyncpg
from transaction import Transaction
from sales import StoreSales
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
        full_namespace = os.getenv("ServiceBusConnection__fullyQualifiedNamespace")
        if not full_namespace:
            logging.critical(
                "ServiceBusConnection__fullyQualifiedNamespace is not set."
            )
            raise ValueError(
                "ServiceBusConnection__fullyQualifiedNamespace environment variable is required."
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
    async def get_pg_connection_string(credential: DefaultAzureCredential) -> str:
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

            async with SecretClient(
                Config.get_key_vault_url(), credential
            ) as key_vault_client:
                # Retrieves the PostgreSQL Credentials from Key Vault and URL encodes them.
                pg_username_secret = await key_vault_client.get_secret(kv_pg_username)
                pg_password_secret = await key_vault_client.get_secret(kv_pg_password)
                pg_username = quote_plus(pg_username_secret.value)
                pg_password = quote_plus(pg_password_secret.value)

            connection_string = f"postgres://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
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


# Global variables
credential = DefaultAzureCredential()
servicebus_client = None
db_connection = None
w3 = None
servicebus_topic_sales_subscription_name = (
    Config.get_servicebus_topic_sales_subscription_name()
)
servicebus_topic_sales_name = Config.get_servicebus_topic_sales_name()
servicebus_topic_axies_name = Config.get_servicebus_topic_axies_name()


async def init_dependencies():
    """
    Initialize dependencies for the function app.
    This function is called when the function app starts.
    """
    global servicebus_client, db_connection, w3

    if not servicebus_client:
        # Initialize Service Bus client and sender
        servicebus_namespace = Config.get_servicebus_full_namespace()
        servicebus_client = ServiceBusClient(
            fully_qualified_namespace=servicebus_namespace,
            credential=credential,
            logging_enable=True,
        )
        logging.info(
            f"Service Bus client initialized for namespace: {servicebus_namespace}"
        )

    if not db_connection:
        # Initialize PostgreSQL connection
        db_connection_string = await Config.get_pg_connection_string(credential)
        db_connection = await asyncpg.create_pool(
            dsn=db_connection_string,
            ssl="require",
            min_size=1,
            max_size=10,
        )
        logging.info("PostgreSQL connection initialized.")

    if not w3:
        # Initialize Web3 provider
        w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(Config.get_node_provider()))
        logging.info("Web3 provider initialized.")


async def close_dependencies():
    """
    Close dependencies for the function app.
    This function is called when the function app shuts down.
    """
    global servicebus_client, servicebus_topic_axies_sender, db_conn

    if servicebus_client:
        await servicebus_client.close()
        logging.info("Service Bus client closed.")

    if db_connection:
        await db_connection.close()
        logging.info("PostgreSQL connection closed.")

    if w3:
        await w3.provider.disconnect()
        logging.info("Web3 provider disconnected.")


app = func.FunctionApp()


@app.service_bus_topic_trigger(
    arg_name="azservicebus",
    subscription_name=servicebus_topic_sales_subscription_name,
    topic_name=servicebus_topic_sales_name,
    connection="ServiceBusConnection",
)
async def store_axie_sales(azservicebus: func.ServiceBusMessage):
    global servicebus_client, db_connection, w3

    # Ensure dependencies are initialized
    await init_dependencies()

    try:
        message_body = ast.literal_eval(azservicebus.get_body().decode("utf-8"))
        logging.info(
            "Python ServiceBus Topic trigger processed a message: %s", message_body
        )

        transaction_hash = message_body["transactionHash"]
        block_number = message_body["blockNumber"]
        block_timestamp = message_body["blockTimestamp"]

        # Call Transaction class to get the sales list from a transaction hash.
        sales_list = await Transaction(db_connection, w3).process_logs(transaction_hash)

        # Call the StoreSales class to store the sales in the database and send message to the axies topic.
        if sales_list:
            await StoreSales(
                db_connection,
                servicebus_client=servicebus_client,
                servicebus_topic_axies_name=servicebus_topic_axies_name,
                sales_list=sales_list,
                block_number=block_number,
                block_timestamp=block_timestamp,
                transaction_hash=transaction_hash,
            ).add_to_db()
        else:
            logging.info("Sales list is empty.")

        logging.info(
            f"All sales of transaction {transaction_hash} have been processed successfuly."
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e
