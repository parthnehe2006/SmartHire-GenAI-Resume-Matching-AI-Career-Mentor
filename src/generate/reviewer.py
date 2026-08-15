import time

from google import genai
from src.config import GEMINI_API_KEY, GEMINI_MODEL


def get_gemini_client():
    api_key = GEMINI_API_KEY

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    api_key = api_key.strip()

    return genai.Client(api_key=api_key)


def review_resume(resume_text, job_description):

    # --------------------------------
    # Validate Input
    # --------------------------------

    if not resume_text or not resume_text.strip():
        return """
### ⚠️ AI Review Error

The uploaded resume does not contain enough readable text
for AI review.
"""

    if not job_description or not job_description.strip():
        return """
### ⚠️ AI Review Error

Please provide a job description before generating
the AI resume review.
"""

    # --------------------------------
    # Limit Very Large Input
    # --------------------------------

    resume_text = resume_text[:20000]
    job_description = job_description[:12000]

    # --------------------------------
    # Create Prompt
    # --------------------------------

    prompt = f"""
You are an expert HR recruiter and resume reviewer.

Analyze the candidate's resume against the target job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Give the analysis using exactly these sections:

## 1. Strengths
Explain the candidate's strongest qualifications relevant to the job.

## 2. Missing Skills
List important skills, technologies, qualifications, or experience
mentioned in the job description but missing or unclear in the resume.

## 3. Weaknesses
Identify weaknesses or areas where the resume could be improved.

## 4. Suggestions
Give specific, practical suggestions to improve the resume for this role.

IMPORTANT RULES:
- Do NOT calculate or provide a match score.
- Do NOT mention any percentage score.
- The application calculates the official match score separately.
- Base the review only on the provided resume and job description.
- Do not invent qualifications or experience.
- Keep the response professional and useful.
"""

    max_attempts = 3
    last_error = None

    # Create client when the function is actually called
    try:
        client = get_gemini_client()
    except Exception as e:
        print(f"Gemini client initialization failed: {e}")
        return """
## ⚠️ AI Review Temporarily Unavailable

The Gemini API configuration could not be initialized.
Please check the API key configuration.
"""

    # --------------------------------
    # Call Gemini with Retry
    # --------------------------------

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            if response is None:
                raise RuntimeError("Gemini returned an empty response.")

            response_text = getattr(response, "text", None)

            if not response_text or not response_text.strip():
                raise RuntimeError(
                    "Gemini returned a response without text."
                )

            return response_text

        except Exception as e:
            last_error = str(e)

            print(
                f"Gemini review attempt "
                f"{attempt + 1}/{max_attempts} failed: "
                f"{last_error}"
            )

            if attempt < max_attempts - 1:
                wait_time = 3 * (attempt + 1)
                time.sleep(wait_time)

    return """
## ⚠️ AI Review Temporarily Unavailable

The resume was successfully parsed and the job matching analysis
was completed.

However, the AI Resume Review service could not generate a response
after multiple attempts.

Please try **Analyze Resume** again in a few moments.

The following parts of SmartHire AI are still available:

- Resume parsing
- Match score calculation
- Skill analysis
- Dataset-based job recommendations
- Resume information
- Career Mentor
- Professional report export
"""