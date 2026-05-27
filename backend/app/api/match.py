from fastapi import APIRouter

from app.schemas.match import MatchRequest, MatchResponse
from app.services.matcher import compute_section_scores

router = APIRouter()


@router.post("/api/match", response_model=MatchResponse)
def match(request: MatchRequest) -> MatchResponse:
    scores = compute_section_scores(request.resume_text, request.job_description)
    return MatchResponse(
        skills=scores.get("skills", 0.0),
        experience=scores.get("experience", 0.0),
        education=scores.get("education", 0.0),
        overall=scores["overall"],
    )
