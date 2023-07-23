from azure.storage.blob import BlobServiceClient
import sanic
from sentence_splitter import SentenceSplitter

from app.core.ml import Predictor
from app.core.security import JWTHandler

__all__ = ["download_artifacts", "load_ml_model", "setup_sentence_splitter"]


def download_artifacts(app: sanic.Sanic) -> None:
    blob_service_client = BlobServiceClient.from_connection_string(app.config.CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(
        container=app.config.AZURE_CONTAINER_NAME, blob=app.config.MODEL_PATH
    )
    stream = blob_client.download_blob()
    with open(app.config.MODEL_PATH, "wb") as fp:
        content = stream.readall()
        fp.write(content)
    app.config.CONNECTION_STRING = None


async def load_ml_model(app: sanic.Sanic) -> None:
    predictor = Predictor(app.config.MODEL_PATH)
    await predictor.async_load()
    app.ctx.predictor = predictor


async def setup_sentence_splitter(app: sanic.Sanic) -> None:
    app.ctx.splitter = SentenceSplitter(language=app.config.TENANT)


async def setup_token_handler(app: sanic.Sanic) -> None:
    app.ctx.token_handler = JWTHandler(secret=app.config.TOKEN_SECRET, issuer=app.config.APP_NAME)
