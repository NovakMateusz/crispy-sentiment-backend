import datetime
import os
import pathlib

from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions


def download_artifact_to_file(
    account_name: str,
    account_key: str,
    container_name: str,
    blob_name: str,
    file_path: pathlib.Path,
) -> None:
    start_time = datetime.datetime.utcnow()
    expiry_time = start_time + datetime.timedelta(minutes=5)
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        start=start_time,
        expiry=expiry_time,
        permission=BlobSasPermissions(read=True),
    )

    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=sas_token
    )
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )
    download_stream = blob_client.download_blob()
    with open(file_path, "wb") as file:
        download_stream.readall()


def upload_artifact_from_file(
    account_name: str,
    account_key: str,
    container_name: str,
    blob_name: str,
    file_path: pathlib.Path,
) -> None:
    start_time = datetime.datetime.utcnow()
    expiry_time = start_time + datetime.timedelta(minutes=5)
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        start=start_time,
        expiry=expiry_time,
        permission=BlobSasPermissions(write=True),
    )

    blob_service_client = BlobServiceClient(
        account_url=account_url, credential=sas_token
    )
    blob_client = blob_service_client.get_blob_client(
        container=container_name, blob=blob_name
    )
    with open(file_path, "rb") as my_blob:
        blob_client.upload_blob(my_blob.read())


import pickle


def download_with_str(connection_string: str, container_name: str, blob_name: str):
    print(type(bytes_output))
    print(pickle.loads(bytes_output))


account_url = os.environ.get(
    "ACCOUNT_URL", "https://crispy0storage0account.blob.core.windows.net"
)
tenant = os.environ.get("TENANT", "en")
container = f"crispy-sentiment-{tenant}"
conn_str = "DefaultEndpointsProtocol=https;AccountName=crispy0storage0account;AccountKey=+z8Xsc3+o0/0LEslfW/ruQtIOQKhs8f60moQFv7kKP9Ivh9yMyF7dhLJkNf1Zk3qXl9u/WGS4JiB+AStQoyrBw==;EndpointSuffix=core.windows.net"
download_with_str(conn_str, "crispy-sentiment-en", "221a10e8df9349be9b2632aa62f348cb")
