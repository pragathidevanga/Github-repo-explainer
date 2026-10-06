from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .job_manager import JobManager
from .llm_service import OllamaService
from .models import AnalyzeQueuedResponse, AnalyzeRequest, JobStatusResponse, RootResponse

BASE_DIR = Path(__file__).resolve().parent.parent
REPOSITORIES_DIR = BASE_DIR / "repositories"
manager = JobManager(REPOSITORIES_DIR)


@asynccontextmanager
async def lifespan(app: FastAPI):
    REPOSITORIES_DIR.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="Local GitHub Repository Code Explainer",
    description="Analyze any public GitHub repository with a locally running Ollama/Qwen model.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=RootResponse)
def root() -> RootResponse:
    llm = OllamaService()
    return RootResponse(
        status="running",
        message="Local GitHub Repository Code Explainer API",
        llm_model=llm.model,
        llm_base_url=llm.base_url,
    )


@app.get("/api/health")
def health() -> dict:
    llm = OllamaService()
    return {"status": "ok", "ollama_available": llm.health(), "model": llm.model}


@app.post("/api/analyze", response_model=AnalyzeQueuedResponse, status_code=202)
def start_analysis(request: AnalyzeRequest) -> AnalyzeQueuedResponse:
    try:
        manager.processor.validate_url(request.github_url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    job = manager.create(request.github_url.strip())
    return AnalyzeQueuedResponse(job_id=job.job_id, message="Analysis started. Poll the job endpoint for progress.")


@app.get("/api/jobs/{job_id}", response_model=JobStatusResponse)
def job_status(job_id: str) -> JobStatusResponse:
    try:
        return manager.as_response(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Analysis job not found.") from exc
