from fastapi import FastAPI
from sentence_splitter import SentenceSplitter
from tortoise import Tortoise

from app.core.ml import Predictor
from app.core.security import JWTHandler
from app.settings import Settings


__all__ = ["init_db", "setup_jwt_handler", "setup_predictor", "setup_splitter", "close_db_connection"]


async def init_db(settings: Settings):
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.core.db.models"]},
    )
    if settings.ENVIRONMENT == "dev":
        await Tortoise.generate_schemas()


def setup_jwt_handler(app: FastAPI, settings: Settings):
    app.state.jwt_handler = JWTHandler(settings.TOKEN_SECRET, settings.APP_NAME)


async def setup_predictor(app: FastAPI, settings: Settings):
    app.state.predictor = Predictor(model_path=settings.MODEL_PATH)
    await app.state.predictor.async_load()


def setup_splitter(app: FastAPI, settings: Settings):
    app.state.splitter = SentenceSplitter(language=settings.TENANT)


async def close_db_connection():
    await Tortoise.close_connections()
