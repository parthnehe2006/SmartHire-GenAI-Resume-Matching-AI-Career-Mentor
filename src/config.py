import os
from dotenv import load_dotenv

# Load local .env file (for VS Code/local development)
load_dotenv()

# Default values for local development
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Try to load Streamlit Cloud secrets
try:
    import streamlit as st

    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    if "GEMINI_MODEL" in st.secrets:
        GEMINI_MODEL = st.secrets["GEMINI_MODEL"]

except Exception:
    # Streamlit secrets are unavailable locally
    pass