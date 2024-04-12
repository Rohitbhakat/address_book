import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import BASE_ROUTE
from models.db import initialize_database
from routers import address_book

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("App starting up..")
    logger.info("Intializing Db")
    initialize_database()

    yield
    logger.info("App Shutting down ..")


app = FastAPI(title="Address Book Rest API", lifespan=lifespan)


app.include_router(address_book.router, prefix=BASE_ROUTE)


@app.get(f"{BASE_ROUTE}/health")
async def get_health_check():
    return {"message": "Server is running"}
