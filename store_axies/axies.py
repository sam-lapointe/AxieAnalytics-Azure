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

    async def __get_axie_data(self) -> dict:
        api_url = "https://api-gateway.skymavis.com/graphql/axie-marketplace"
        headers = {
            "accept": "application/json, multipart/mixed",
            "content-type": "application/json",
            "x-api-key": self.__api_key
        }
        body = f"""{{
            "query":"query MyQuery($lastNDays: Int = 30) {{\\n  axie(axieId: \\"{self.__axie_id}\\") {{\\n    earnedAxpStat(lastNDays: $lastNDays)\\n    bodyShape\\n    breedCount\\n    class\\n    title\\n    parts {{\\n      id\\n    }}\\n    image\\n    axpInfo {{\\n      level\\n      xp\\n    }}\\n  }}\\n}}",
            "operationName":"MyQuery",
            "variables":{{}}
        }}"""

        try:
            async with aiohttp.ClientSession as http_client:
                async with http_client.post(api_url, headers=headers, data=body) as axie_data_response:
                    axie_data = await axie_data_response.json()
                    logging.info(axie_data)
        except Exception as e:
            logging.error(
                f"[__get_axie_data] Error fetching axie data: {e}"
            )
            raise e
        
    async def store_axie_data(self) -> None:
        pass