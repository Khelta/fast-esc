from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from fastesc.configuration import TEST_DATABASE_URL, API_KEY
from fastesc.database.models import models
from fastesc.database.models.base import Base
from fastesc.db import get_db_session
from fastesc.main import app
from tests.data import country_import_data, contest_import_data, song_import_data

models


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture()
async def fill_database(client, country_import_data, contest_import_data, song_import_data):
    await client.post("/data_import/countries/",
                      json=country_import_data,
                      headers={"Authorization": f"Bearer {API_KEY}"})

    await client.post("/data_import/contests/",
                      json=contest_import_data,
                      headers={"Authorization": f"Bearer {API_KEY}"})

    await client.post("/data_import/songs/",
                      json=song_import_data,
                      headers={"Authorization": f"Bearer {API_KEY}"})
