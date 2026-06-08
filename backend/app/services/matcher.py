import re

import numpy as np
from fastembed import TextEmbedding

_model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Maps a canonical section name to the header keywords that identify it in the text.
SECTION_KEYWORDS = {
    "skills": ["skills", "technical skills", "core competencies"],
    "experience": ["experience", "work experience", "employment history", "professional experience"],
    "education": ["education", "academic background", "qualifications"],
}


def compute_similarity(resume_text: str, job_description_text: str) -> float:
    """Embed both texts and return their cosine similarity, clamped to [0, 1]."""
    resume_embedding, job_embedding = _model.embed([resume_text, job_description_text])
    score = np.dot(resume_embedding, job_embedding) / (
        np.linalg.norm(resume_embedding) * np.linalg.norm(job_embedding)
    )
    return max(0.0, min(1.0, float(score)))


def parse_sections(text: str) -> dict:
    """Split text into Skills/Experience/Education sections via simple header keyword matching.

    Scans each line; if it looks like a header (short line matching a known keyword),
    everything until the next recognized header is collected under that section.
    """
    sections = {name: "" for name in SECTION_KEYWORDS}
    current_section = None
    buffers = {name: [] for name in SECTION_KEYWORDS}

    for line in text.splitlines():
        stripped = line.strip().strip(":").lower()
        matched_section = None
        if stripped and len(stripped) <= 40:
            for section_name, keywords in SECTION_KEYWORDS.items():
                if stripped in keywords:
                    matched_section = section_name
                    break

        if matched_section:
            current_section = matched_section
            continue

        if current_section and line.strip():
            buffers[current_section].append(line.strip())

    for name in SECTION_KEYWORDS:
        sections[name] = "\n".join(buffers[name])

    return sections


def compute_section_scores(resume_text: str, job_description_text: str) -> dict:
    """Score resume vs. job description per section, plus an overall score.

    Returns a dict like {"skills": 0.85, "experience": 0.79, "education": 0.91, "overall": 0.83}.
    Sections missing from either text are skipped.
    """
    resume_sections = parse_sections(resume_text)
    job_sections = parse_sections(job_description_text)

    scores = {}
    for section_name in SECTION_KEYWORDS:
        resume_section = resume_sections[section_name]
        job_section = job_sections[section_name]
        if resume_section and job_section:
            scores[section_name] = compute_similarity(resume_section, job_section)

    scores["overall"] = compute_similarity(resume_text, job_description_text)
    return scores
