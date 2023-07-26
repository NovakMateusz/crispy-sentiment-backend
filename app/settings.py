import os
import pathlib

__all__ = ["Settings"]


class Settings:
    APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment-backend")
    APP_VERSION = "v0.1.0"
    TENANT = os.environ.get("TENANT", "en")
    ENVIRONMENT = os.environ.get("ENVIRONMENT", 'dev')

    MODEL_HASH = os.environ.get("MODEL_HASH", "dev_artifact")
    ARTIFACTS_BASE_PATH = os.environ.get("ARTIFACTS_BASE_PATH", "app/artifacts")
    MODEL_PATH = pathlib.Path(ARTIFACTS_BASE_PATH) / MODEL_HASH

    S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "https://s3.filebase.com")
    BUCKET_NAME = os.environ.get("BUCKET_NAME", "crispy-sentiment")
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")

    TOKEN_SECRET = os.environ.get("TOKEN_SECRET", "SuperSecretSecret")

    DB_URL = os.environ.get("DB_URL", "sqlite://:memory:")
