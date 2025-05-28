# resume_utils.py
import fitz  # PyMuPDF

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)
