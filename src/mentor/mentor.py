from google import genai

from src.config import GEMINI_API_KEY, GEMINI_MODEL
from src.mentor.rag_chain import retrieve_career_notes
from src.safety.guardrails import check_question


# --------------------------------
# Get Gemini Client
# --------------------------------

def get_gemini_client():

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing.")

    return genai.Client(
        api_key=GEMINI_API_KEY.strip()
    )


# --------------------------------
# AI Career Mentor
# --------------------------------

def ask_career_mentor(question):

    # --------------------------------
    # Guardrails
    # --------------------------------

    guardrail_result = check_question(question)

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

    context = "\n\n".join(context_parts)


    # --------------------------------
    # Career Mentor Prompt
    # --------------------------------

    prompt = f"""
You are SmartHire AI Career Mentor.

Your job is to help students with career-related questions.

IMPORTANT RULES:

1. Answer using ONLY the retrieved career notes provided below.

2. Do not invent information that is not present in the
retrieved notes.

3. If the retrieved notes do not contain enough information
to answer the question, say:

"I don't have enough information in my career knowledge
base to answer that question."

4. Keep the answer practical and easy to understand.

5. Use headings, bullet points, or numbered steps when useful.

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

        client = get_gemini_client()

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        if not response or not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text


    except Exception as e:

        print(f"Career Mentor Gemini error: {e}")

        return (
            "⚠️ Unable to generate the mentor "
            "response right now.\n\n"
            "Please try again in a few moments."
        )


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    question = input(
        "Ask the AI Career Mentor: "
    )

    answer = ask_career_mentor(question)

    print("\nCareer Mentor Answer:")
    print("---------------------")
    print(answer)