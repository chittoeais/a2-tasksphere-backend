from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncMongoClient(settings.MONGODB_URL)
    app.database = app.mongodb_client[settings.MONGODB_DB_NAME]

    ping = await app.database.command("ping")
    if int(ping["ok"]) != 1:
        raise Exception("MongoDB connection failed")

    yield

    app.mongodb_client.close()