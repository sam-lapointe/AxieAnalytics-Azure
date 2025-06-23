from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.core import config
from src.database import db
from src.routes import axie_sales


@asynccontextmanager
async def lifespan(app: FastAPI):
    await config.Config.init_secrets()
    db.database = db.Postgres(config.db_connection_string)
    await db.database.connect()
    yield
    await db.database.disconnect()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(axie_sales.router, prefix="/axies", tags=["Axies"])