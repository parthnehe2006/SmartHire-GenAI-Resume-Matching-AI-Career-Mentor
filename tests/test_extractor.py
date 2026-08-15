from src.parsing.loader import extract_text_from_pdf
from src.parsing.preprocess import clean_text
from src.parsing.extractor import extract_name, extract_email, extract_phone, extract_skills


pdf = "data/resumes/sample_resume.pdf"

text = extract_text_from_pdf(pdf)
text = clean_text(text)

print("Name :", extract_name(text))
print("Email:", extract_email(text))
print("Phone:", extract_phone(text))
print("Skills:", extract_skills(text))