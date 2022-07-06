import io

from random_receipt.utils import convert_html_to_jpeg_byte_array


def test_convert_html_to_jpeg_byte_array_succeeds():
    with open("tests/data/document.html", "r") as f:
        html_document = f.read()

    assert isinstance(convert_html_to_jpeg_byte_array(html_document), io.BytesIO)
