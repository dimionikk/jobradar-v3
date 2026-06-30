from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.vacancy import VacancyOut
from app.models.applications import ApplicationStatus


class ApplicationOut(BaseModel):
    id: int
    status: ApplicationStatus
    note: Optional[str] = None
    applied_at: datetime
    vacancy: VacancyOut
    model_config = ConfigDict(from_attributes=True)


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    note: Optional[str] = None