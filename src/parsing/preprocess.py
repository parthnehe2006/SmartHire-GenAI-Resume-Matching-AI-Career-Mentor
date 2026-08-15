import re

def clean_text(text):
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted symbols (keep ., ,, -, /)
    text = re.sub(r"[^a-zA-Z0-9@.,;:/+\-\s]", "", text)

    return text.strip()