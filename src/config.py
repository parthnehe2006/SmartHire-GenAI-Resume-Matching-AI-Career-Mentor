import os
from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st

    GEMINI_API_KEY = st.secrets.get(
        "GEMINI_API_KEY",
        os.getenv("GEMINI_API_KEY")
    )

    GEMINI_MODEL = st.secrets.get(
        "GEMINI_MODEL",
        os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    )

except Exception:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")