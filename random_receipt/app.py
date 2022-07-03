import io
import os
import uuid

from flask import Flask, jsonify, render_template
from weasyprint import HTML
import boto3

from random_receipt.receipt import generate


app = Flask(__name__)


@app.route("/api/receipt")
def generate_random_receipt():
    receipt = generate()
    receipt_html_str = render_template("receipt.html", **receipt)
    receipt_pdf = HTML(string=receipt_html_str).write_pdf()

    # upload to s3 and generate presigned url
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    s3_client = session.client("s3")
    filename = str(uuid.uuid4()) + ".pdf"
    s3_client.upload_fileobj(
        io.BytesIO(receipt_pdf), os.getenv("S3_BUCKET"), filename
    )
    presigned_url = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": os.getenv("S3_BUCKET"), "Key": filename},
        ExpiresIn=100000
    )

    receipt["imageUrl"] = presigned_url
    receipt["imageFilename"] = filename
    return jsonify(receipt)


if __name__ == "__main__":
    app.run(debug=False)
