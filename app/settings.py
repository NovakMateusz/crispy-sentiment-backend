import os
import pathlib


class Settings:
    APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment-backend")
    TENANT = os.environ.get("TENANT", "en")

    DB_URL = os.environ.get("DB_URL", "sqlite://:memory:")
    GENERATE_DB_SCHEMAS = bool(os.environ.get("GENERATE_DB_SCHEMAS", True))

    TOKEN_SECRET = os.environ.get("TOKEN_SECRET", "SuperSecretSecret")

    MODEL_HASH = os.environ.get("MODEL_HASH", "dev_artifact")
    ARTIFACTS_PATH = pathlib.Path(os.environ.get("ARTIFACTS_PATH", pathlib.Path("artifacts")))
    MODEL_PATH = ARTIFACTS_PATH / MODEL_HASH
