"""
Pydantic models for the FastAPI endpoints.
# Pydantic validates input automatically — saves me writing manual checks
"""

from typing import Optional
from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str
    history: list = []   # list of [question, answer] pairs from previous turns


class AskResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float
    icd_categories: list[str]
    specialist: Optional[str] = None


class ClassifyRequest(BaseModel):
    symptoms: str


class ClassifyResponse(BaseModel):
    icd_categories: list[str]
    specialist: str
    confidence: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str = "1.0.0"
