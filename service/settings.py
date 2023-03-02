import os
import pathlib


class Settings:
    APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment")

    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
    S3_ENDPOINT = os.environ.get("S3_ENDPOINT", "https://s3.filebase.com")
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    MODEL_HASH = os.environ.get("MODEL_HASH", "Testing")
    ARTIFACTS_PATH = pathlib.Path(os.environ.get("ARTIFACTS_PATH", pathlib.Path("artifacts")))
    MODEL_PATH = ARTIFACTS_PATH / MODEL_HASH