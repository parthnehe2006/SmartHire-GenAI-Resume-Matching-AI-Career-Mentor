from src.generate.reviewer import review_resume

job = """
Python Developer

Skills Required:
- Python
- Machine Learning
- SQL
- TensorFlow
- Docker
"""

resume = """
Python Developer with Machine Learning and SQL experience.
Worked on TensorFlow projects.
"""

result = review_resume(resume, job)

print(result)