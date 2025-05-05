import asyncpg
import logging
from datetime import datetime, timezone


class StoreSales:
    """
    Add sales to DB and call send_message to alert axies service.
    """

    def __init__(
        self,
        conn: asyncpg.Connection,
        sales_list: list,
        block_number: int,
        block_timestamp: int,
        transaction_hash: str,
    ):
        self.__conn = conn
        self.__sales_list = sales_list
        self.__block_number = block_number
        self.__block_timestamp = block_timestamp
        self.__transaction_hash = transaction_hash

    async def add_to_db(self) -> None:
        if not self.__sales_list:
            logging.warning("Sales list is empty. No data to add to DB.")
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

                await self.__conn.execute(
                    """
                    INSERT INTO contracts(
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
                logging.info(f"Added to DB Axie sale: {axie_sale}")

                self.__send_topic_message()

            except Exception as e:
                logging.error(
                    f"An unexpected error occured while adding to DB Axie sale {sale}: {e}"
                )
                raise e

        logging.info(
            f"All sales were added to the database successfuly for transaction {self.__transaction_hash}."
        )
        return

    def __send_topic_message(self, axie_sale) -> None:
        logging.info("Sending message to axies topic...")
        pass
