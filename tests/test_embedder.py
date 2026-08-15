from src.vectorstore.embedder import get_embedding

text = "Python developer with Machine Learning skills"

embedding = get_embedding(text)

print("Embedding length:", len(embedding))
print(embedding[:10])