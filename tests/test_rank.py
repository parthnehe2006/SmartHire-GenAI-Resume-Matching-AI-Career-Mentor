from src.search.rank_resume import similarity

job = """
Python Developer
Machine Learning
TensorFlow
SQL
"""

resume = """
Python developer with Machine Learning skills and SQL experience.
"""

score = similarity(job, resume)

print("Similarity Score:", score)