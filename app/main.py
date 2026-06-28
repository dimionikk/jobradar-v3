from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth, profile, ai, saved_vacancies, applications
from contextlib import asynccontextmanager
from app.core.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, lifespan=lifespan)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(ai.router)
app.include_router(saved_vacancies.router)
app.include_router(applications.router)
