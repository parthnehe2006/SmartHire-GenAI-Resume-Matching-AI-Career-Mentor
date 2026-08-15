from src.generate.matcher import calculate_match_score

resume = """
Python
Java
SQL
Machine Learning
Data Analysis
"""

job = """
Looking for Python developer with SQL and Machine Learning.
"""

score = calculate_match_score(resume, job)

print("Match Score:", score, "%")