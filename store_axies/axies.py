import logging
import asyncpg
import aiohttp
from asyncpg.exceptions import UniqueViolationError
from datetime import datetime, timezone


class Axie:
    """
    Represent an axie and provide methods to gather and store informationa about it.
    """

    def __init__(
        self,
        conn: asyncpg.Connection,
        api_key: str,
        transaction_hash: str,
        axie_id: int,
        sale_date: int,
    ):
        self.__conn = conn
        self.__api_key = api_key
        self.__transaction_hash = transaction_hash
        self.__axie_id = axie_id
        self.__sale_date = sale_date

    async def get_axie_data(self) -> dict:
        pass
