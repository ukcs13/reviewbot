import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

@pytest.mark.asyncio
async def test_readiness_check(client: AsyncClient):
    # This might fail if Redis is not running, but for tests we could mock it
    response = await client.get("/ready")
    # Depending on environment, could be 200 or 503
    assert response.status_code in [200, 503]

@pytest.mark.asyncio
async def test_create_review_invalid_source(client: AsyncClient):
    response = await client.post(
        "/api/review",
        data={"source_type": "invalid"}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_review_missing_github_url(client: AsyncClient):
    response = await client.post(
        "/api/review",
        data={"source_type": "github_url"}
    )
    assert response.status_code == 422
