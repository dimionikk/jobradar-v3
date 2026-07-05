from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, profile, ai, saved_vacancies, applications, vacancies
from contextlib import asynccontextmanager
from app.core.scheduler import scheduler
from app.core.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()
    await redis_client.aclose()


app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://app.89-167-93-204.nip.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(ai.router)
app.include_router(saved_vacancies.router)
app.include_router(applications.router)
app.include_router(vacancies.router)