from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(resume_text: str, job_description_text: str) -> float:
    """Embed both texts and return their cosine similarity, clamped to [0, 1]."""
    embeddings = _model.encode([resume_text, job_description_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return max(0.0, min(1.0, score))
