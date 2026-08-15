import os

from dotenv import load_dotenv
from google import genai

from src.mentor.rag_chain import retrieve_career_notes
from src.safety.guardrails import check_question


# --------------------------------
# Load Environment Variables
# --------------------------------

load_dotenv()


# --------------------------------
# Gemini Client
# --------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )

client = genai.Client(
    api_key=api_key
)


# --------------------------------
# AI Career Mentor
# --------------------------------

def ask_career_mentor(question):

    # --------------------------------
    # Guardrails
    # --------------------------------

    guardrail_result = check_question(
        question
    )

    if not guardrail_result["allowed"]:

        return guardrail_result["message"]


    # --------------------------------
    # Retrieve Career Notes
    # --------------------------------

    results = retrieve_career_notes(
        question,
        k=3
    )


    # --------------------------------
    # Check Retrieved Results
    # --------------------------------

    if not results:

        return (
            "I don't have enough information in "
            "my career knowledge base to answer "
            "that question."
        )


    # --------------------------------
    # Build Context
    # --------------------------------

    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['content']}"
        )


    context = "\n\n".join(
        context_parts
    )


    # --------------------------------
    # Career Mentor Prompt
    # --------------------------------

    prompt = f"""
You are SmartHire AI Career Mentor.

Your job is to help students with career-related
questions.

IMPORTANT RULES:

1. Answer using ONLY the retrieved career notes
   provided below.

2. Do not invent information that is not present
   in the retrieved notes.

3. If the retrieved notes do not contain enough
   information to answer the question, say:

"I don't have enough information in my career
knowledge base to answer that question."

4. Keep the answer practical and easy to understand.

5. Use headings, bullet points, or numbered steps
   when useful.

6. Stay focused on career-related topics.

7. Mention the source document when useful.


--------------------------------
RETRIEVED CAREER NOTES
--------------------------------

{context}


--------------------------------
USER QUESTION
--------------------------------

{question}


--------------------------------
ANSWER
--------------------------------
"""


    # --------------------------------
    # Generate Gemini Response
    # --------------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            "⚠️ Unable to generate the mentor "
            "response right now.\n\n"
            f"Error: {str(e)}"
        )


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    question = input(
        "Ask the AI Career Mentor: "
    )

    answer = ask_career_mentor(
        question
    )

    print("\n")
    print("Career Mentor Answer:")
    print("---------------------")
    print(answer)