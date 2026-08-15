import re

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if match:
        return match.group()
    return "Not Found"


def extract_phone(text):
    match = re.search(r'(\+?\d[\d\-\s]{8,}\d)', text)
    if match:
        return match.group()
    return "Not Found"


def extract_name(text):
    lines = text.split()

    blacklist = [
    "functional",
    "resume",
    "sample",
    "career",
    "summary",
    "education",
    "experience",
    "skills",
    "employment"
]
    name = []

    for word in lines:
        if word.lower() in blacklist:
            continue

        if word[0].isupper():
            name.append(word)

        if len(name) == 3:
            break

    return " ".join(name)    
    
def extract_skills(text):
    skills_db = [
        "Python", "Java", "C", "C++", "SQL",
        "Machine Learning", "Deep Learning",
        "Data Analysis", "TensorFlow", "PyTorch",
        "Excel", "Power BI", "Communication",
        "Leadership", "Teamwork"
    ]

    found = []

    lower_text = text.lower()

    for skill in skills_db:
        if skill.lower() in lower_text:
            found.append(skill)

    return found    

