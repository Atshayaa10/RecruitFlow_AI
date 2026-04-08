import pypdf
import io

def extract_text_from_pdf(pdf_file: bytes) -> str:
    """Extracts text from a PDF file using pypdf."""
    reader = pypdf.PdfReader(io.BytesIO(pdf_file))
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text.strip()
