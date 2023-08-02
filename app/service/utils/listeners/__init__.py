import sanic
from sentence_splitter import SentenceSplitter

from app.core.security import JWTHandler
from app.core.ml import Predictor

__all__ = ["setup_token_handler", "load_ml_model", "setup_splitter"]


async def setup_token_handler(app: sanic.Sanic) -> None:
    app.ctx.token_handler = JWTHandler(secret=app.config.TOKEN_SECRET, issuer=app.config.APP_NAME)


async def load_ml_model(app: sanic.Sanic) -> None:
    predictor = Predictor(app.config.MODEL_PATH)
    await predictor.async_load()
    app.ctx.predictor = predictor


async def setup_splitter(app: sanic.Sanic) -> None:
    app.ctx.splitter = SentenceSplitter(language=app.config.TENANT)
