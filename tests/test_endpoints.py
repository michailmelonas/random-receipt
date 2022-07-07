import os

import boto3
import pytest

from random_receipt.app import app


@pytest.fixture()
def app_client():
    return app.test_client()


@pytest.fixture()
def s3_client():
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return session.client("s3")


def test_random_receipt_endpoint(app_client):
    response = app_client.get("/api/receipt")

    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_random_receipt_endpoint_uploads_pdf_to_s3(app_client, s3_client):
    response = app_client.get("/api/receipt")
    s3_client.head_object(Bucket=os.getenv("S3_BUCKET"), Key=response.json["imageFilename"])


def test_random_receipt_endpoint_contains_image_url(app_client):
    response = app_client.get("/api/receipt")
    assert "imageUrl" in response.json.keys()
