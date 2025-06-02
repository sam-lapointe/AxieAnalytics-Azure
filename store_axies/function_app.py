import azure.functions as func
import logging
import asyncpg
import ast
from datetime import datetime, timezone
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from config import Config
from parts import Part
from axies import Axie


# Global variables
credential = DefaultAzureCredential()
db_connection = None
servicebus_topic_axies_subscription_name = (
    Config.get_servicebus_topic_axies_subscription_name()
)
servicebus_topic_axies_name = Config.get_servicebus_topic_axies_name()
api_key = Config.get_axie_api_key(credential)


async def init_dependencies():
    """
    Initialize dependencies for the function app.
    This function is called when the function app starts.
    """
    global db_connection

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

    # Verify if the versions table contain the current version of parts
    current_parts_version = await Part.get_current_version(db_connection)
    if not current_parts_version:
        await Part.search_and_update_parts_latest_version(db_connection)


app = func.FunctionApp()


@app.service_bus_topic_trigger(
    arg_name="azservicebus",
    subscription_name=servicebus_topic_axies_subscription_name,
    topic_name=servicebus_topic_axies_name,
    connection="ServiceBusConnection",
) 
async def store_axies(azservicebus: func.ServiceBusMessage):
    global db_connection, api_key

    # Ensure dependencies are initialized
    await init_dependencies()

    message_body = ast.literal_eval(azservicebus.get_body().decode("utf-8"))
    logging.info(
        "Python ServiceBus Topic trigger processed a message: %s", message_body
    )

    # Process the axie data
    await Axie(
        db_connection,
        api_key,
        message_body["transaction_hash"],
        message_body["axie_id"],
        message_body["sale_date"],
    ).process_axie_data()


@app.timer_trigger(
    arg_name="timer",
    schedule="0 */1 * * * *",  # Every minute
    use_monitoring=False,
)
def timer_function(timer: func.TimerRequest) -> None:
    """
    Time function to keep the function app alive.
    """
    current_time_utc = datetime.now(timezone.utc)
    logging.info("Python timer trigger function ran at %s", current_time_utc)
    # This function is used to keep the function app alive.
    # It does not do anything else.
    # It is called every minute.