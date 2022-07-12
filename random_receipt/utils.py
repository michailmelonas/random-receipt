import io

from weasyprint import HTML


def convert_html_to_pdf_byte_array(document_html: str) -> io.BytesIO:
    pdf = HTML(string=document_html).write_pdf()
    byte_array = io.BytesIO(pdf)
    return byte_array
