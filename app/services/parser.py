import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vacancy import Vacancy
from app.services.embeddings import embed_documents

logger = logging.getLogger(__name__)

UPDATABLE_FIELDS = ("title", "description", "company", "city", "salary", "work_type", "experience")
STALE_CUTOFF_DAYS = 7


async def save_vacancies(vacancies: list[dict], db: AsyncSession) -> dict:
    new_count = 0
    skipped_count = 0
    invalid_count = 0

    valid_items = []
    urls = []
    for vacancy_data in vacancies:
        url = vacancy_data.get("url")
        title = vacancy_data.get("title")
        if not url or not title:
            invalid_count += 1
            continue
        valid_items.append(vacancy_data)
        urls.append(url)

    existing_by_url = {}
    if urls:
        result = await db.execute(select(Vacancy).where(Vacancy.url.in_(urls)))
        existing_by_url = {v.url: v for v in result.scalars().all()}

    new_vacancies = []
    for vacancy_data in valid_items:
        url = vacancy_data["url"]
        existing = existing_by_url.get(url)

        if existing:
            for field in UPDATABLE_FIELDS:
                if field in vacancy_data:
                    setattr(existing, field, vacancy_data[field])
            existing.parsed_at = datetime.now(timezone.utc)
            existing.is_active = True
            skipped_count += 1
            continue

        try:
            new_vacancy = Vacancy(**vacancy_data)
        except TypeError:
            logger.exception("Invalid vacancy data, skipping: url=%s", url)
            invalid_count += 1
            continue

        new_vacancies.append(new_vacancy)
        new_count += 1

    if new_vacancies:
        texts = [f"{v.title}. {v.description or ''}" for v in new_vacancies]
        try:
            embeddings = await embed_documents(texts)
            for vacancy, embedding in zip(new_vacancies, embeddings):
                vacancy.embedding = embedding
        except Exception:
            logger.exception("Failed to generate embeddings for %s new vacancies", len(new_vacancies))

        for vacancy in new_vacancies:
            db.add(vacancy)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        logger.exception("Failed to commit vacancies batch (new=%s, skipped=%s)", new_count, skipped_count)
        return {"new": 0, "skipped": 0, "invalid": len(vacancies)}

    return {"new": new_count, "skipped": skipped_count, "invalid": invalid_count}


async def deactivate_stale_vacancies(db: AsyncSession, cutoff_days: int = STALE_CUTOFF_DAYS) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(days=cutoff_days)
    result = await db.execute(
        update(Vacancy)
        .where(Vacancy.parsed_at < cutoff, Vacancy.is_active.is_(True))
        .values(is_active=False)
    )
    await db.commit()
    return result.rowcount