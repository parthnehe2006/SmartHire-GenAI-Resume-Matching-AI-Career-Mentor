from sklearn.metrics.pairwise import cosine_similarity
from src.vectorstore.embedder import get_embedding
import numpy as np


def similarity(job_text, resume_text):
    job_emb = np.array(get_embedding(job_text)).reshape(1, -1)
    resume_emb = np.array(get_embedding(resume_text)).reshape(1, -1)

    score = cosine_similarity(job_emb, resume_emb)

    return float(score[0][0])