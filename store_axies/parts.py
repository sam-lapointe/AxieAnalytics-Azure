import logging
import asyncpg
import aiohttp
from datetime import datetime, timedelta


class Part:
    @staticmethod
    async def get_part(conn: asyncpg.Connection, part_id: str) -> dict:
        logging.info(f"[get_part] Fetching data for part {part_id} from database...")
        try:
            async with conn.acquire() as conn:
                part = await conn.fetchrow("SELECT * FROM users WHERE id = $1", part_id)
            return part
        except Exception as e:
            logging.error(
                f"[get_part] An unexpected error occured while fetching part {part_id}: {e}"
            )
            raise e
        
    @staticmethod
    async def get_current_version(conn: asyncpg.Connection) -> datetime.date:
        # Create new table for the current version of parts
        pass

    @staticmethod
    async def search_parts_update(conn: asyncpg.Connection, days: int, current_version: datetime) -> tuple[str, datetime.date, dict]:
        """
        This method should be used on demand to verify if there was an update to the parts from Axie Infinity today.
        """
        logging.info(f"[search_parts_update] Verifying if there was an update to Axies parts in the last {days} days...")
        current_date = datetime.now().date()

        try:
            for i in range(0, days + 1):
                date = current_date - timedelta(days=i)
                date_str = date.strftime("%Y%m%d")

                if current_version > date:
                    logging.info(f"[search_parts_update] Stopping the search, current version is up to date.")
                    return None, None, {}

                parts_url = f"https://cdn.axieinfinity.com/game/origin-cards/base/origin-cards-data-{date_str}/part_data.json"
                async with aiohttp.ClientSession as http_client:
                    async with http_client.get(parts_url) as axie_parts_response:
                        if axie_parts_response.status != 404:
                            logging.info("[search_parts_update] There is a new update to parts, returning it...")
                            axie_parts = await axie_parts_response.json()
                            return parts_url, date, axie_parts

            logging.info(f"[search_parts_update] No new parts update was found in the last {days} days.")
            return None, None, {}
        except Exception as e:
            logging.error(
                f"[search_parts_update] An unexpected error occured while fetching the list of parts: {e}"
            )
            raise e

    @staticmethod
    async def update_parts(conn: asyncpg.Connection, parts: dict, url: str) -> None:
        logging.info("[update_parts] Updating the axie_parts table...")

        # Update the current version of parts

        # Compare the new version of parts with the parts in database and update.