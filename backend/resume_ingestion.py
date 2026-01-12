import pdfplumber
import re
import io


def extract_pdf_content(file_bytes: bytes) -> str:
    extracted_text = []

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text.append(page_text)

    return "\n".join(extracted_text)


def clean_resume_text(raw_text: str) -> str:
    text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[=*\-_]{3,}", "", text)
    text = re.sub(r"\t+", " ", text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)


def load_resume(file_bytes: bytes) -> dict:
    raw_text = extract_pdf_content(file_bytes)
    cleaned_text = clean_resume_text(raw_text)

    return {"text": cleaned_text, "length": len(cleaned_text.split())}
