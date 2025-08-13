import pytest
from httpx import ASGITransport, AsyncClient

from fastesc.main import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API. Visit /docs for documentation."}
