import azure.functions as func
import logging
import asyncpg
import ast
from datetime import datetime, timezone
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from config import Config


# Global variables
credential = DefaultAzureCredential()
db_connection = None
servicebus_topic_axies_subscription_name = (
    Config.get_servicebus_topic_axies_subscription_name()
)
servicebus_topic_axies_name = Config.get_servicebus_topic_axies_name()


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


app = func.FunctionApp()


@app.service_bus_topic_trigger(
    arg_name="azservicebus",
    subscription_name=servicebus_topic_axies_subscription_name,
    topic_name=servicebus_topic_axies_name,
    connection="ServiceBusConnection",
) 
async def store_axies(azservicebus: func.ServiceBusMessage):
    global db_connection

    # Ensure dependencies are initialized
    await init_dependencies()

    try:
        message_body = ast.literal_eval(azservicebus.get_body().decode("utf-8"))
        logging.info(
            'Python ServiceBus Topic trigger processed a message: %s', message_body
        )

        # TODO: Verify if the axie_parts table is filled, fill it if it is not
        # TODO: Get the axie information from Axie Graphql
        # TODO: Verify the Axie Level, Ascension and Evolved parts at the time of sale
        # TODO: Store the data
        # TODO: Add another timer trigger function to verify the axie parts and update them if needed.


    except Exception as e:
        logging.error(f"An unexpected error occured: {e}")
        raise e


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