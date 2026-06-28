from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from app.schemas.vacancy import VacancyOut


class ApplicationOut(BaseModel):
    id: int
    status: str
    note: Optional[str] = None
    applied_at: datetime
    vacancy: VacancyOut

    model_config = ConfigDict(from_attributes=True)

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    note: Optional[str] = None