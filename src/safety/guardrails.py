import re


# ============================================
# Unsafe / harmful keywords
# ============================================

UNSAFE_KEYWORDS = [
    "hack",
    "hacking",
    "malware",
    "virus",
    "ransomware",
    "phishing",
    "exploit",
    "ddos",
    "steal password",
    "steal passwords",
    "credit card fraud",
    "identity theft",
    "bomb",
    "weapon",
    "kill",
    "murder",
    "suicide",
    "self harm",
    "drugs",
]


# ============================================
# Career-related keywords
# ============================================

CAREER_KEYWORDS = [
    "career",
    "job",
    "jobs",
    "resume",
    "cv",
    "interview",
    "internship",
    "intern",
    "skill",
    "skills",
    "developer",
    "programmer",
    "software",
    "engineer",
    "engineering",
    "data analyst",
    "data scientist",
    "machine learning",
    "artificial intelligence",
    "ai",
    "generative ai",
    "python",
    "java",
    "javascript",
    "sql",
    "cloud",
    "devops",
    "web development",
    "backend",
    "frontend",
    "full stack",
    "placement",
    "placements",
    "college",
    "student",
    "learning",
    "roadmap",
    "project",
    "projects",
    "salary",
    "skills",
    "certification",
]


# ============================================
# Check for unsafe content
# ============================================

def contains_unsafe_content(question):
    """
    Returns True if the question contains
    potentially unsafe content.
    """

    question_lower = question.lower()

    for keyword in UNSAFE_KEYWORDS:

        if keyword in question_lower:

            return True

    return False


# ============================================
# Check whether question is career-related
# ============================================

def is_career_related(question):
    """
    Returns True if the question appears
    to be related to careers, jobs, learning,
    resumes, interviews, or professional growth.
    """

    question_lower = question.lower()

    for keyword in CAREER_KEYWORDS:

        if keyword in question_lower:

            return True

    return False


# ============================================
# Main Guardrail Function
# ============================================

def check_question(question):
    """
    Validate a user question before sending it
    to the AI Career Mentor.

    Returns:

        {
            "allowed": True/False,
            "message": "..."
        }
    """

    # ----------------------------------------
    # Empty question
    # ----------------------------------------

    if not question:

        return {
            "allowed": False,
            "message": "Please enter a question."
        }


    # Remove unnecessary spaces

    question = question.strip()


    if not question:

        return {
            "allowed": False,
            "message": "Please enter a question."
        }


    # ----------------------------------------
    # Question length
    # ----------------------------------------

    if len(question) > 1000:

        return {
            "allowed": False,
            "message": (
                "Your question is too long. "
                "Please keep it under 1000 characters."
            )
        }


    # ----------------------------------------
    # Unsafe content check
    # ----------------------------------------

    if contains_unsafe_content(question):

        return {
            "allowed": False,
            "message": (
                "⚠️ I can't help with unsafe or harmful requests. "
                "Please ask a career, job, resume, interview, "
                "or professional-development question."
            )
        }


    # ----------------------------------------
    # Career relevance check
    # ----------------------------------------

    if not is_career_related(question):

        return {
            "allowed": False,
            "message": (
                "🤖 I'm the AI Career Mentor. "
                "I can help with careers, jobs, resumes, "
                "interviews, skills, internships, projects, "
                "and professional development."
            )
        }


    # ----------------------------------------
    # Question allowed
    # ----------------------------------------

    return {
        "allowed": True,
        "message": "Question passed the safety check."
    }


# ============================================
# Test
# ============================================

if __name__ == "__main__":

    test_questions = [

        "How can I become a machine learning engineer?",

        "How should I improve my resume?",

        "What skills do I need for a data analyst job?",

        "How can I prepare for an interview?",

        "How can I hack someone's account?",

        "What is the weather today?",
    ]


    for question in test_questions:

        result = check_question(question)

        print("\nQuestion:", question)

        print("Allowed:", result["allowed"])

        print("Message:", result["message"])