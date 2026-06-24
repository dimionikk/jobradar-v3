from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.include_router(auth.router)
