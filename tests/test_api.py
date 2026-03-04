"""
API tests for HealthRAG.
Run with: pytest tests/ -v
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_health_endpoint():
    """GET /health should return 200 with status ok."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


@pytest.mark.anyio
async def test_ask_valid_query():
    """POST /ask with a real medical question should return an answer."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/ask",
            json={"query": "what is diabetes", "history": []}
        )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert len(data["answer"]) > 10  # should have a real answer


@pytest.mark.anyio
async def test_ask_empty_query():
    """POST /ask with an empty query should return 422 validation error."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/ask",
            json={"query": "", "history": []}
        )

    assert response.status_code in [422, 400]


@pytest.mark.anyio
async def test_classify_endpoint():
    """POST /classify with symptoms should return ICD-10 categories."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/classify",
            json={"symptoms": "fever and cough"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "icd_categories" in data
    assert "specialist" in data


@pytest.mark.anyio
async def test_non_medical_query():
    """POST /ask with a non-medical question should politely decline."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/ask",
            json={"query": "write me a poem about the ocean", "history": []}
        )

    assert response.status_code == 200
    data = response.json()
    # the system should say it only handles medical questions
    answer_lower = data["answer"].lower()
    assert any(phrase in answer_lower for phrase in [
        "only answer medical",
        "medical questions",
        "health-related",
    ])
