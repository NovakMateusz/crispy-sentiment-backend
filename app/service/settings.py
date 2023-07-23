import os
import pathlib


# class Settings:
#     APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment")
#     TENANT = os.environ.get("TENANT")

#     # Azure
#     CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
#     AZURE_CONTAINER_NAME = f"crispy-sentiment-{TENANT}"

#     MODEL_HASH = os.environ.get("MODEL_HASH", "Testing")
#     ARTIFACTS_PATH = pathlib.Path(os.environ.get("ARTIFACTS_PATH", pathlib.Path("app/artifacts")))
#     MODEL_PATH = ARTIFACTS_PATH / MODEL_HASH

class Settings:
    APP_NAME = os.environ.get("APP_NAME", "crispy-sentiment-backend")
    TENANT = os.environ.get("TENANT", "en")

    CONNECTION_STRING = os.environ.get("CONNECTION_STRING", "DefaultEndpointsProtocol=https;AccountName=crispy0storage0account;AccountKey=+z8Xsc3+o0/0LEslfW/ruQtIOQKhs8f60moQFv7kKP9Ivh9yMyF7dhLJkNf1Zk3qXl9u/WGS4JiB+AStQoyrBw==;EndpointSuffix=core.windows.net")
    AZURE_CONTAINER_NAME = f"crispy-sentiment-{TENANT}"

    MODEL_HASH = os.environ.get("MODEL_HASH", "221a10e8df9349be9b2632aa62f348cb")
    ARTIFACTS_PATH = pathlib.Path(os.environ.get("ARTIFACTS_PATH", pathlib.Path("app/artifacts")))
    MODEL_PATH = ARTIFACTS_PATH / MODEL_HASH

    TOKEN_SECRET = os.environ.get("TOKEN_SECRET", "SuperSecretSecret")