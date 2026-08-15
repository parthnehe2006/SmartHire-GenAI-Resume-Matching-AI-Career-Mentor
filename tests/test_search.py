from src.search.search_resume import search_resume

query = "Python Machine Learning"

results = search_resume(query)

print("Matching resumes:")

for r in results:
    print(r)
    