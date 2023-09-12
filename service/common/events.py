import datetime

from loguru import logger
from fastapi import FastAPI


def startup():
    logger.info(f"fastapi startup at {datetime.datetime.now()}")


def shutdown():
    logger.info(f"fastapi shutdown at {datetime.datetime.now()}")


def register_events(app: FastAPI):
    app.add_event_handler("startup", startup)
    app.add_event_handler("shutdown", shutdown)
