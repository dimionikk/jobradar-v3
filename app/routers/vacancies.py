import logging

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.limiter import limiter
from app.models.vacancy import Vacancy
from app.schemas.vacancy import VacancyOut
from app.services.embeddings import embed_query

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/vacancies", tags=["Vacancies"])


@router.get("/", response_model=list[VacancyOut])
@limiter.limit("30/minute")
async def get_vacancies(
    request: Request,
    search: str | None = None,
    city: str | None = None,
    source: str | None = None,
    work_type: str | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Vacancy).where(Vacancy.is_active.is_(True))

    if city:
        query = query.where(Vacancy.city.ilike(f"%{city}%"))
    if source:
        query = query.where(Vacancy.source == source)
    if work_type:
        query = query.where(Vacancy.work_type.ilike(f"%{work_type}%"))

    if search:
        try:
            query_vector = await embed_query(search)
            query = query.where(Vacancy.embedding.is_not(None))
            query = query.order_by(Vacancy.embedding.cosine_distance(query_vector))
        except Exception:
            logger.exception("Semantic search failed for query=%r, falling back to text search", search)
            query = query.where(
                or_(
                    Vacancy.title.ilike(f"%{search}%"),
                    Vacancy.description.ilike(f"%{search}%"),
                )
            )
            query = query.order_by(Vacancy.created_at.desc())
    else:
        query = query.order_by(Vacancy.created_at.desc())

    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    vacancies = result.scalars().all()
    return vacancies