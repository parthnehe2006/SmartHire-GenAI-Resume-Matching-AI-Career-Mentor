from src.parsing.resume_parser import parse_resume

pdf = "data/resumes/current_resume.pdf"

result = parse_resume(pdf)

for key, value in result.items():
    print(f"{key}: {value}")