from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.match import router as match_router

app = FastAPI(title="Resume-Job Match Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(match_router)
