from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.vacancy import Vacancy
from app.services.embeddings import embed_documents


async def save_vacancies(vacancies: list[dict], db: AsyncSession) -> dict:
    new_count = 0
    skipped_count = 0
    invalid_count = 0
    new_vacancies = []

    for vacancy_data in vacancies:
        url = vacancy_data.get("url")
        title = vacancy_data.get("title")
        if not url or not title:
            invalid_count += 1
            continue

        result = await db.execute(select(Vacancy).where(Vacancy.url == url))
        existing = result.scalar_one_or_none()
        if existing:
            existing.parsed_at = datetime.now(timezone.utc)
            skipped_count += 1
            continue

        new_vacancy = Vacancy(**vacancy_data)
        new_vacancies.append(new_vacancy)
        new_count += 1

    if new_vacancies:
        texts = [
            f"{v.title}. {v.description or ''}"
            for v in new_vacancies
        ]
        try:
            embeddings = await embed_documents(texts)
            for vacancy, embedding in zip(new_vacancies, embeddings):
                vacancy.embedding = embedding
        except Exception as e:
            print(f"Не вдалося згенерувати ембединги: {e}")

        for vacancy in new_vacancies:
            db.add(vacancy)

    await db.commit()
    return {"new": new_count, "skipped": skipped_count, "invalid": invalid_count}