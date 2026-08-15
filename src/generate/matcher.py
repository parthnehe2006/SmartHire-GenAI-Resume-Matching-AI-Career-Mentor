from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def extract_keywords(text):
    """
    Extract important technical keywords from text.
    """

    skills = [
        "python",
        "java",
        "c++",
        "c",
        "sql",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "generative ai",
        "llm",
        "langchain",
        "llamaindex",
        "faiss",
        "chromadb",
        "pinecone",
        "sentence transformers",
        "embeddings",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas",
        "scikit-learn",
        "fastapi",
        "flask",
        "streamlit",
        "docker",
        "git",
        "github",
        "rest api",
        "api"
    ]

    text = text.lower()

    found = []

    for skill in skills:

        # Special handling for programming languages
        if skill == "c++":
            pattern = r"(?<!\w)c\+\+(?!\w)"

        elif skill == "c":
            pattern = r"(?<!\w)c(?!\w)"

        else:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


def calculate_match_score(resume_text, job_text):
    """
    Calculate resume-job match score.

    60% = Semantic similarity
    40% = Skill matching
    """

    # 1. Semantic similarity
    resume_embedding = model.encode([resume_text])
    job_embedding = model.encode([job_text])

    semantic_score = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    semantic_score = max(0, min(1, semantic_score))
    semantic_percentage = semantic_score * 100

    # 2. Skill matching
    resume_skills = set(extract_keywords(resume_text))
    job_skills = set(extract_keywords(job_text))

    matched_skills = resume_skills.intersection(job_skills)
    missing_skills = job_skills - resume_skills

    if job_skills:
        skill_percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100
    else:
        skill_percentage = 0

    # 3. Final score
    final_score = (
        semantic_percentage * 0.60
        + skill_percentage * 0.40
    )

    return {
        "final_score": round(final_score, 2),
        "semantic_score": round(semantic_percentage, 2),
        "skill_score": round(skill_percentage, 2),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills)
    }