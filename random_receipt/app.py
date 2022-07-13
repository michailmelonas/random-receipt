import datetime
import os
import uuid

from flask import Flask, jsonify, render_template
import boto3

from random_receipt.receipt import generate
from random_receipt.utils import convert_html_to_pdf_byte_array


app = Flask(__name__)


@app.route("/api/receipt")
def generate_random_receipt():
    receipt = generate()
    receipt_html = render_template("receipt.html", **receipt)
    byte_array = convert_html_to_pdf_byte_array(receipt_html)

    # upload to s3
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    s3_client = session.client("s3")
    filename = str(uuid.uuid4()) + ".pdf"
    s3_client.upload_fileobj(
        byte_array,
        os.getenv("S3_BUCKET"),
        filename,
        ExtraArgs={"ContentType": "application/pdf"},
    )

    receipt["pdfFilename"] = filename
    receipt["pdfUrl"] =  f"https://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/{filename}"
    receipt["datestamp"] = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
    return jsonify(receipt)


if __name__ == "__main__":
    app.run(debug=False)
