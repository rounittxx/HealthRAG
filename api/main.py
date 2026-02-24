"""
FastAPI backend for HealthRAG.
Three endpoints: /ask, /classify, /health
# loading models at startup so first request isn't slow
"""

import os
import time
import sys
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load .env before importing anything that reads config
from dotenv import load_dotenv
load_dotenv()

from api.schemas import AskRequest, AskResponse, ClassifyRequest, ClassifyResponse, HealthResponse
from rag.rag_pipeline import RAGPipeline
from classifier.inference import classify_symptoms
from classifier.specialist_router import recommend_specialist

# simple in-memory rate limiting (no Redis yet — TODO for production)
_request_counts = defaultdict(list)
RATE_LIMIT = 30       # max requests per window
RATE_WINDOW = 60      # seconds


def check_rate_limit(ip: str):
    now = time.time()
    # clean up old requests outside the window
    _request_counts[ip] = [t for t in _request_counts[ip] if now - t < RATE_WINDOW]

    if len(_request_counts[ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a moment.")

    _request_counts[ip].append(now)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup — load everything once
    print("Starting HealthRAG API...")
    try:
        app.state.pipeline = RAGPipeline()
        app.state.model_loaded = True
        print("Models loaded successfully!")
    except Exception as e:
        print(f"[!] Model loading failed: {e}")
        print("    Starting with model_loaded=False — some endpoints will return errors")
        app.state.pipeline = None
        app.state.model_loaded = False

    yield
    # shutdown
    print("Shutting down HealthRAG API")


app = FastAPI(
    title="HealthRAG API",
    description="AI-powered medical Q&A system using RAG + BioBERT",
    version="1.0.0",
    lifespan=lifespan,
)

# allow all origins so the Streamlit frontend can hit it freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "something went wrong", "detail": str(exc)}
    )


@app.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    return HealthResponse(
        status="ok",
        model_loaded=request.app.state.model_loaded
    )


@app.post("/ask", response_model=AskResponse)
async def ask(request: Request, body: AskRequest):
    """
    Main endpoint: takes a medical question + chat history,
    returns an evidence-based answer with sources and specialist recommendation.
    """
    if not body.query.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty")

    check_rate_limit(request.client.host)

    if not request.app.state.model_loaded or request.app.state.pipeline is None:
        raise HTTPException(status_code=503, detail="Models not loaded yet. Please try again shortly.")

    result = request.app.state.pipeline.get_answer(
        query=body.query,
        chat_history=body.history or []
    )

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"],
        icd_categories=result["icd_categories"],
        specialist=result.get("specialist"),
    )


@app.post("/classify", response_model=ClassifyResponse)
async def classify(request: Request, body: ClassifyRequest):
    """
    Classifies symptom text to ICD-10 categories and recommends a specialist.
    Useful for standalone symptom triage without the full RAG answer.
    """
    if not body.symptoms.strip():
        raise HTTPException(status_code=422, detail="Symptoms cannot be empty")

    check_rate_limit(request.client.host)

    icd_results = classify_symptoms(body.symptoms)
    specialist, _ = recommend_specialist(icd_results)

    icd_categories = [cat for cat, _ in icd_results if cat != "Unknown"]
    top_confidence = icd_results[0][1] if icd_results else 0.0

    return ClassifyResponse(
        icd_categories=icd_categories,
        specialist=specialist,
        confidence=round(top_confidence, 4),
    )
