from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyOut

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/", response_model=list[VacancyOut])
async def get_vacancies(
    city: str | None = None,
    source: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Vacancy).where(Vacancy.is_active.is_(True))

    if city:
        query = query.where(Vacancy.city.ilike(f"%{city}%"))
    if source:
        query = query.where(Vacancy.source == source)

    query = query.order_by(Vacancy.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    vacancies = result.scalars().all()
    return vacancies
