from src.parsing.loader import extract_text_from_pdf
from src.parsing.preprocess import clean_text

pdf_path = "data/resumes/sample_resume.pdf"

text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(text)

print(cleaned_text)