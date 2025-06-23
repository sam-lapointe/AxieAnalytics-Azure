import asyncpg
import logging
from fastapi import FastAPI
from typing import Optional


database = None


class Postgres:
    def __init__(self, db_connection_string: str):
        self.db_connection_string = db_connection_string


    async def connect(self):
        self.pool = await asyncpg.create_pool(
            dsn=self.db_connection_string,
            ssl="require",
            min_size=1,
            max_size=10,
        )


    async def disconnect(self):
        await self.pool.close()
