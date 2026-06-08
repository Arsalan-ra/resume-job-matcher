# Resume-Job Match Predictor

A web application that scores how well a resume aligns with a job description. It returns
both an overall fit score and a section-level breakdown across skills, experience, and
education, computed via sentence embeddings and cosine similarity.

## Live Demo

- Frontend: https://resume-job-matcher-gray.vercel.app
- API: https://resume-job-matcher-mgab.onrender.com/docs

## Features

- Overall match score between a resume and a job description, in the range 0-1
- Section-level scoring for skills, experience, and education, derived by parsing each
  document into sections and scoring the corresponding sections against each other
- Single-endpoint REST API (`POST /api/match`) with request/response validation via
  Pydantic schemas
- React frontend for pasting resume and job description text and viewing results as an
  overall score plus per-section progress bars

## Tech Stack

**Backend**
- Python, FastAPI, Uvicorn
- `sentence-transformers` (`all-MiniLM-L6-v2`) for text embeddings, with cosine similarity
  via `sentence_transformers.util`
- Pydantic for request/response schemas
- pytest for testing

**Frontend**
- React 19
- Vite
- Tailwind CSS 4

## Architecture Overview

The system is a thin client-server application built around a single matching operation:

1. The React frontend collects resume text and job description text from the user and
   POSTs them to the backend as JSON (`frontend/src/services/api.js`).
2. The FastAPI backend (`backend/app/api/match.py`) validates the request against the
   `MatchRequest` schema and delegates to the matching service.
3. The matching service (`backend/app/services/matcher.py`):
   - Parses each document into `skills`, `experience`, and `education` sections by
     scanning for recognizable section headers (`parse_sections`).
   - Encodes the relevant text pairs with a `SentenceTransformer` model and computes
     cosine similarity, clamped to `[0, 1]` (`compute_similarity`).
   - Combines per-section scores with an overall score computed from the full documents
     (`compute_section_scores`).
4. The response is serialized through the `MatchResponse` schema and returned to the
   client, which renders the overall score and per-section bars (`ScoreBar.jsx`).

There is no persistence layer; each request is stateless and scored independently. The
sentence-transformer model is loaded once at import time and reused across requests.

## How to Run Locally

### Backend

From `backend/`:

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with the match endpoint at
`POST /api/match`. It expects a JSON body of the form:

```json
{
  "resume_text": "...",
  "job_description": "..."
}
```

To run the test script directly:

```bash
python test_matcher.py
```

### Frontend

From `frontend/`:

```bash
npm install
npm run dev
```

The dev server runs on Vite's default port (typically `http://localhost:5173`) and
expects the backend to be running at `http://127.0.0.1:8000` (configured in
`frontend/src/services/api.js`).

Run both the backend and frontend servers concurrently to use the application end to end.

## Project Structure

```
resume-job-matcher/
├── backend/
│   ├── requirements.txt
│   ├── test_matcher.py
│   └── app/
│       ├── main.py                  # FastAPI app instance, CORS, router registration
│       ├── api/
│       │   └── match.py             # POST /api/match endpoint
│       ├── schemas/
│       │   └── match.py             # MatchRequest / MatchResponse pydantic models
│       └── services/
│           └── matcher.py           # Section parsing, embedding, and scoring logic
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx                  # Main UI: text inputs, analyze action, results
        ├── components/
        │   └── ScoreBar.jsx         # Labeled progress bar for a single score
        └── services/
            └── api.js               # fetchMatchScores: POST wrapper around /api/match
```
