import asyncpg
import logging
import time


class StoreSales:
    def __init__(self, conn: asyncpg.Connection, sales_list: list, block_number: int, block_timestamp: int):
        self.__conn = conn
        self.__sales_list = sales_list
        self.__block_number = block_number
        self.__block_timestamp = block_timestamp

    
    """
    Add sales to DB and call send_message to alert axies service.
    This might be better as a classmethod.
    """
    def add_to_db(self):
        for sale in self.__sales_list:
            logging.info("Added: {sale}")
        pass


    def send_topic_message(self):
        logging.info("Sending message to Axies topic...")
        pass