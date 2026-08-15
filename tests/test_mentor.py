from src.mentor.mentor import career_mentor

resume = """
Python Developer
Skills:
Python
Machine Learning
TensorFlow
SQL
"""

question = "What skills should I learn next to become an AI Engineer?"

answer = career_mentor(resume, question)

print(answer)
