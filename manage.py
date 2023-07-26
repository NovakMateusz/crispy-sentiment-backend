from enum import Enum
import subprocess
from typing import Callable

import boto3
import typer
from typing_extensions import Annotated

from app.settings import Settings

settings = Settings()


class Stage(str, Enum):
    download = "download"


def _download_stage() -> None:
    s3_client = boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.ACCESS_KEY,
        aws_secret_access_key=settings.SECRET_ACCESS_KEY,
    )
    with open(settings.MODEL_PATH, "wb") as fp:
        s3_client.download_fileobj(settings.BUCKET_NAME, f"{settings.TENANT}/{settings.MODEL_HASH}", fp)


def _stage_factory(stage_name: Stage) -> Callable[[], None]:
    match stage_name:
        case Stage.download:
            return _download_stage
        case Stage.build:
            return _build_stage


def main(stage: Annotated[Stage, typer.Argument()]):
    stage_function = _stage_factory(stage)
    stage_function()


if __name__ == "__main__":
    typer.run(main)
