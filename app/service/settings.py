import os
import pathlib


class Settings:
    APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment")
    TENANT = os.environ.get("TENANT")

    # Azure
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
    AZURE_CONTAINER_NAME = f"crispy-sentiment-{TENANT}"

    MODEL_HASH = os.environ.get("MODEL_HASH", "Testing")
    ARTIFACTS_PATH = pathlib.Path(os.environ.get("ARTIFACTS_PATH", pathlib.Path("app/artifacts")))
    MODEL_PATH = ARTIFACTS_PATH / MODEL_HASH
