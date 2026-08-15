from src.parsing.loader import extract_text_from_pdf

pdf_path = "data/resumes/sample_resume.pdf"

text = extract_text_from_pdf(pdf_path)

print("=" * 60)
print("RESUME TEXT")
print("=" * 60)

print(text)