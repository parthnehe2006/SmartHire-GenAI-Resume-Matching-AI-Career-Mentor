from src.parsing.loader import extract_text_from_pdf
from src.parsing.preprocess import clean_text
from src.parsing.extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
)

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    text = clean_text(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text,
    }