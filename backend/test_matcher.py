from app.services.matcher import compute_similarity

SAMPLE_RESUME = """
Experienced backend engineer with 5 years building scalable REST APIs in Python.
Skilled in Python, FastAPI, Django, PostgreSQL, Docker, AWS, and Git.
"""

SAMPLE_JOB_DESCRIPTION = """
We are looking for a Backend Software Engineer to join our growing team.
Required: Python, FastAPI, PostgreSQL, Docker. Familiarity with AWS is a plus.
"""

if __name__ == "__main__":
    score = compute_similarity(SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)
    print(f"Overall similarity score: {score:.4f}")
