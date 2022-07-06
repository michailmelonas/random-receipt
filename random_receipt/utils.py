import io

from pdf2image import convert_from_bytes
from weasyprint import HTML


def convert_html_to_jpeg_byte_array(document_html: str) -> io.BytesIO:
    pdf = HTML(string=document_html).write_pdf()
    images = convert_from_bytes(pdf)
    byte_array = io.BytesIO()
    images[0].save(byte_array, format="JPEG", subsampling=0, quality=50)
    byte_array.seek(0)
    return byte_array
