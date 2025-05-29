import logging
import asyncpg
import aiohttp
from asyncpg.exceptions import UniqueViolationError
from datetime import datetime, timezone
import time


xp_per_level = {
    "1": 100,
    "2": 210,
    "3": 430,
    "4": 740,
    "5": 1140,
    "6": 1640,
    "7": 2260,
    "8": 2980,
    "9": 3810,
    "10": 4760,
    "11": 5830,
    "12": 7010,
    "13": 8320,
    "14": 9760,
    "15": 11310,
    "16": 13010,
    "17": 14830,
    "18": 16780,
    "19": 18870,
    "20": 21090,
    "21": 23460,
    "22": 25950,
    "23": 28600,
    "24": 31380,
    "25": 34300,
    "26": 37380,
    "27": 40590,
    "28": 43950,
    "29": 47470,
    "30": 51130,
    "31": 54940,
    "32": 58910,
    "33": 63020,
    "34": 67300,
    "35": 71720,
    "36": 76300,
    "37": 81040,
    "38": 85940,
    "39": 91000,
    "40": 96210,
    "41": 101590,
    "42": 107130,
    "43": 112820,
    "44": 118700,
    "45": 124720,
    "46": 130920,
    "47": 137280,
    "48": 143800,
    "49": 150500,
    "50": 157370,
    "51": 164390,
    "52": 171600,
    "53": 178970,
    "54": 186520,
    "55": 194240,
    "56": 202120,
    "57": 210190,
    "58": 218430,
    "59": 226840,
    "60": 235430
}


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
            "query":"query MyQuery($lastNDays: Int = 30) {{\\n  axie(axieId: \\"{self.__axie_id}\\") {{\\n    earnedAxpStat(lastNDays: $lastNDays)\\n    bodyShape\\n    breedCount\\n    class\\n    title\\n    parts {{\\n      id\\n      stage\\n    }}\\n    image\\n    axpInfo {{\\n      level\\n      xp\\n    }}\\n  }}\\n}}",
            "operationName":"MyQuery",
            "variables":{{}}
        }}"""

        try:
            async with aiohttp.ClientSession() as http_client:
                async with http_client.post(api_url, headers=headers, data=body) as axie_data_response:
                    axie_data = await axie_data_response.json()
                    logging.info(axie_data)
            return axie_data
        except Exception as e:
            logging.error(
                f"[__get_axie_data] Error fetching axie data: {e}"
            )
            raise e
        
    async def __estimate_axie_level(self, axie_data) -> int:
        """
        Estimate the axie level at time of sale.
        """
        logging.info(
            f"[__estimate_axie_level] Estimating axie level at sale..."
        )
        pass

    async def __verify_last_evolutions(self, axie_data) -> dict:
        """
        Verify the parts stages at time of sale.
        """
        logging.info(
            f"[__verify_last_evolutions] Verifying parts stages at sale..."
        )
        pass
        
    async def __store_axie_data(self, axie_data) -> None:
        pass
        
    async def process_axie_data(self) -> None:
        axie_data = await self.__get_axie_data()

        # Verify if the sale was not made within the last 2 minutes
        current_epoch = int(time.time())
        if current_epoch >= self.__sale_date + 120:
            logging.info(
                f"[process_axie_data] The sale was not made within the last 120 seconds."
            )
            # TODO: If earnedAxpStat estimate the axie level at time of sale.
            #       And verify if it was ascended after the time of sale
            # TODO: If parts at stage > 1, verify if it was upgraded after the time of sale
            pass
        
        # TODO: Store the axie data
        self.__store_axie_data(axie_data)

# Example of axie_data
"""
{
    'data': {
        'axie': {
            'earnedAxpStat': {
                '2025-05-28': [
                    {'source_id': '7', 'xp': 5024}
                ]
            },
            'bodyShape': 'Normal',
            'breedCount': 0,
            'class': 'Reptile',
            'title': '',
            'parts': [
                {'id': 'eyes-tricky', 'stage': 1},
                {'id': 'ears-curly', 'stage': 1},
                {'id': 'mouth-peace-maker', 'stage': 1},
                {'id': 'horn-lagging', 'stage': 1},
                {'id': 'back-indian-star', 'stage': 1},
                {'id': 'tail-koi', 'stage': 1}
            ],
            'image': 'https://assets.axieinfinity.com/axies/11393467/axie/axie-full-transparent.png',
            'axpInfo': {'level': 13, 'xp': 1106}
        }
    }
}
"""