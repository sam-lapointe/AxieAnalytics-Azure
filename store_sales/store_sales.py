import asyncpg
import logging
from asyncpg.exceptions import UniqueViolationError
from datetime import datetime, timezone
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient


class StoreSales:
    """
    Add sales to DB and call send_message to alert axies service.
    """

    def __init__(
        self,
        conn: asyncpg.Connection,
        servicebus_client: ServiceBusClient,
        axies_topic_name: str,
        sales_list: list,
        block_number: int,
        block_timestamp: int,
        transaction_hash: str,
    ):
        self.__conn = conn
        self.__servicebus_client = servicebus_client
        self.__axies_topic_name = axies_topic_name
        self.__sales_list = sales_list
        self.__block_number = block_number
        self.__block_timestamp = block_timestamp
        self.__transaction_hash = transaction_hash

    async def add_to_db(self) -> None:
        """
        Go through the list of sales and add each of them to the database.
        """
        if not self.__sales_list:
            logging.warning("[add_to_db] Sales list is empty. No data to add to DB.")
            return

        for sale in self.__sales_list:
            try:
                current_time_utc = datetime.now(timezone.utc)

                axie_sale = {
                    "block_number": self.__block_number,
                    "transaction_hash": self.__transaction_hash,
                    "sale_date": self.__block_timestamp,
                    "price_eth": sale["price_weth"],
                    "axie_id": sale["axie_id"],
                    "created_at": current_time_utc,
                    "modified_at": current_time_utc,
                }

                try:
                    await self.__conn.execute(
                        """
                        INSERT INTO axie_sales(
                            block_number,
                            transaction_hash,
                            sale_date,
                            price_eth,
                            axie_id,
                            created_at,
                            modified_at                      
                        )
                        VALUES (
                            $1, $2, $3, $4, $5, $6, $7
                        )
                        """,
                        *axie_sale.values(),
                    )
                    logging.info(f"[add_to_db] Added to DB Axie sale: {axie_sale}")
                except UniqueViolationError:
                    logging.info(
                        f"[add_to_db] This axie sale already exists in the database: {axie_sale}"
                    )

                await self.__send_topic_message(axie_sale)

            except Exception as e:
                logging.error(
                    f"[add_to_db] An unexpected error occured while adding to DB Axie sale {axie_sale}: {e}"
                )
                raise e

        logging.info(
            f"[add_to_db] All sales were added to the database successfuly for transaction {self.__transaction_hash}."
        )
        return

    async def __send_topic_message(self, axie_sale) -> None:
        """
        For each sale, sends a message to axies topic.
        """
        try:
            async with self.__servicebus_client.get_topic_sender(
                self.__axies_topic_name
            ) as sender:
                message = {
                    "transaction_hash": self.__transaction_hash,
                    "axie_id": axie_sale["axie_id"],
                }

                # Send message to the Axies topic.
                await sender.send_messages(ServiceBusMessage(str(message)))
            logging.info(f"[__send_topic_message] Sent message: {message}")
        except Exception as e:
            logging.error(
                f"[__send_topic_message] An unexpected error occured while sending message to axies topic for {axie_sale}: {e}"
            )
            raise e
