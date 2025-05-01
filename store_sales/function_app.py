import azure.functions as func
import logging
import os
import ast
import aiohttp
import asyncpg
from transaction import Transaction
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


# Authenticate to Azure
credential = DefaultAzureCredential()
key_vault_client = SecretClient(Config.get_key_vault_url(), credential)

# Servicebus Variables
servicebus_topic_subscription_name = Config.get_servicebus_topic_subscription_name()
servicebus_topic_name = Config.get_servicebus_topic_name()


app = func.FunctionApp()

@app.service_bus_topic_trigger(arg_name="azservicebus", subscription_name=servicebus_topic_subscription_name,
                               topic_name=servicebus_topic_name, connection="ServiceBusConnection") 
def store_axie_sales(azservicebus: func.ServiceBusMessage):
    message_body = ast.literal_eval(azservicebus.get_body().decode('utf-8'))
    logging.info('Python ServiceBus Topic trigger processed a message: %s', message_body)

    transaction_hash = message_body["transactionHash"]

    # TODO: Call Transaction class to get the sales list


    # TODO: Cale the StoreSales class to store the sales in the database
