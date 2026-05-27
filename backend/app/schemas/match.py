from pydantic import BaseModel


class MatchRequest(BaseModel):
    resume_text: str
    job_description: str


class MatchResponse(BaseModel):
    skills: float
    experience: float
    education: float
    overall: float
