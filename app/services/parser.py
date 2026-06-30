from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.vacancy import Vacancy


async def save_vacancies(vacancies: list[dict], db: AsyncSession) -> dict:
    new_count = 0
    skipped_count = 0
    for vacancy_data in vacancies:
        url = vacancy_data.get("url")
        if not url:
            continue
        result = await db.execute(select(Vacancy).where(Vacancy.url == url))
        existing = result.scalar_one_or_none()
        if existing:
            existing.parsed_at = datetime.now(timezone.utc)
            skipped_count += 1
            continue
        new_vacancy = Vacancy(**vacancy_data)
        db.add(new_vacancy)
        new_count += 1
    await db.commit()
    return {"new": new_count, "skipped": skipped_count}