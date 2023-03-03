import boto3
import sanic
from sentence_splitter import SentenceSplitter

from app.core.ml import Predictor

__all__ = ["download_artifacts", "load_ml_model", "setup_sentence_splitter"]


async def download_artifacts(app: sanic.Sanic) -> None:
    s3_client = boto3.client(
        "s3",
        endpoint_url=app.config.S3_ENDPOINT,
        aws_access_key_id=app.config.ACCESS_KEY,
        aws_secret_access_key=app.config.SECRET_ACCESS_KEY,
    )
    with open(app.config.MODEL_PATH, "wb") as fp:
        s3_client.download_fileobj(app.config.BUCKET_NAME, f"{app.config.TENANT}/{app.config.MODEL_HASH}", fp)


async def load_ml_model(app: sanic.Sanic) -> None:
    predictor = Predictor(app.config.MODEL_PATH)
    await predictor.async_load()
    app.ctx.predictor = predictor


async def setup_sentence_splitter(app: sanic.Sanic) -> None:
    app.ctx.splitter = SentenceSplitter(language=app.config.TENANT)
