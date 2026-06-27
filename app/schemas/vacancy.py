from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class VacancyOut(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    city: Optional[str] = None
    salary: Optional[str] = None
    work_type: Optional[str] = None
    description: Optional[str] = None
    url: str
    source: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)