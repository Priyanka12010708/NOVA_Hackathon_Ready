import fitz
from PIL import Image
import pytesseract


def extract_text_from_pdf(uploaded_file):
    """Extract text from an uploaded PDF."""
    file_bytes = uploaded_file.read()

    document = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages).strip()


def extract_text_from_image(uploaded_file):
    """Extract text from an uploaded image using OCR."""
    image = Image.open(uploaded_file)

    text = pytesseract.image_to_string(image)

    return text.strip()