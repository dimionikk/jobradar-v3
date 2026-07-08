import os
import uuid
from dotenv import load_dotenv

load_dotenv()

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

os.environ["DATABASE_URL"] = (
    os.environ["DATABASE_URL"]
    .replace("/jobradar-db", "/jobradar-test-db")
    .replace(":5432", ":5433")
)

from app.main import app
from app.core.database import Base, get_db
from app.core.redis_client import redis_client
from app.core.limiter import limiter
from app.models.vacancy import Vacancy

limiter.enabled = False


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    engine = create_async_engine(os.environ["DATABASE_URL"])
    session_local = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with session_local() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    yield

    await redis_client.flushdb()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_headers(client):
    payload = {"email": "user@example.com", "password": "testpassword123"}
    await client.post("/auth/register", json=payload)
    login_response = await client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def seed_vacancies():
    async def _seed(count=3, **overrides):
        engine = create_async_engine(os.environ["DATABASE_URL"])
        session_local = async_sessionmaker(bind=engine, expire_on_commit=False)
        ids = []
        async with session_local() as session:
            for i in range(count):
                data = {
                    "title": f"Python Developer {i}",
                    "company": "TestCorp",
                    "city": "Kyiv",
                    "source": "djinni",
                    **overrides,
                }
                data["url"] = f"https://example.com/vacancy/{uuid.uuid4()}"
                vacancy = Vacancy(**data)
                session.add(vacancy)
                await session.flush()
                ids.append(vacancy.id)
            await session.commit()
        await engine.dispose()
        return ids
    return _seed