import re


def load_jd(text: str) -> dict:
    if not text or not text.strip():
        raise ValueError("Job description is empty")

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[=*\-_]{3,}", "", text)
    text = re.sub(r"\t+", " ", text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    cleaned = "\n".join(lines)

    return {"job_description": cleaned, "length": len(cleaned.split())}
