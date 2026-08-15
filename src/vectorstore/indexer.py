import os
import faiss
import numpy as np

from src.parsing.resume_parser import parse_resume
from src.vectorstore.embedder import get_embedding

resume_folder = "data/resumes"

embeddings = []
filenames = []

for file in os.listdir(resume_folder):
    if file.endswith(".pdf"):
        path = os.path.join(resume_folder, file)

        data = parse_resume(path)

        embedding = get_embedding(data["text"])

        embeddings.append(embedding)
        filenames.append(file)

embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "vectorstore/resume.index")

with open("vectorstore/files.txt", "w") as f:
    for file in filenames:
        f.write(file + "\n")

print("Index created successfully!")
print("Total resumes:", len(filenames))