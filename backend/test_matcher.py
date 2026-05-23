from app.services.matcher import compute_similarity, compute_section_scores

SAMPLE_RESUME = """
Experienced backend engineer with 5 years building scalable REST APIs in Python.

Skills
Python, FastAPI, Django, PostgreSQL, Docker, AWS, Git

Experience
Backend Engineer at Acme Corp (2020-2025)
Led a team that migrated a monolithic service to microservices, improving
response times by 40%. Built and maintained REST APIs serving millions of requests.

Education
Bachelor's degree in Computer Science, State University (2020)
"""

SAMPLE_JOB_DESCRIPTION = """
We are looking for a Backend Software Engineer to join our growing team.

Skills
Required: Python, FastAPI, PostgreSQL, Docker. Familiarity with AWS is a plus.

Experience
3+ years designing and maintaining REST APIs in a production environment.
Experience with microservices architecture is preferred.

Education
Bachelor's degree in Computer Science or a related field.
"""

if __name__ == "__main__":
    score = compute_similarity(SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)
    print(f"Overall similarity score: {score:.4f}")

    section_scores = compute_section_scores(SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)
    print(f"Section scores: {section_scores}")
