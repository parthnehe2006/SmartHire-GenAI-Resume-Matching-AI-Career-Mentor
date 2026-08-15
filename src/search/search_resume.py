import faiss
import numpy as np

from src.vectorstore.embedder import get_embedding

index = faiss.read_index("vectorstore/resume.index")

with open("vectorstore/files.txt", "r") as f:
    files = [line.strip() for line in f.readlines()]


def search_resume(query, k=3):
    query_embedding = np.array([get_embedding(query)]).astype("float32")

    # Don't ask for more results than available resumes
    k = min(k, len(files))

    distances, indices = index.search(query_embedding, k)

    results = []

    for idx in indices[0]:
        if idx != -1 and idx < len(files):
            results.append(files[idx])

    return results