import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.vacancy import Vacancy
from app.services.embeddings import embed_documents

BATCH_SIZE = 50


async def backfill():
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Vacancy).where(Vacancy.embedding.is_(None))
        )
        vacancies = result.scalars().all()

        if not vacancies:
            print("Усі вакансії вже мають ембединги.")
            return

        print(f"Знайдено {len(vacancies)} вакансій без ембедингів.")

        for i in range(0, len(vacancies), BATCH_SIZE):
            batch = vacancies[i:i + BATCH_SIZE]
            texts = [f"{v.title}. {v.description or ''}" for v in batch]

            embeddings = await embed_documents(texts)
            for vacancy, embedding in zip(batch, embeddings):
                vacancy.embedding = embedding

            await db.commit()
            print(f"Оброблено {min(i + BATCH_SIZE, len(vacancies))}/{len(vacancies)}")


if __name__ == "__main__":
    asyncio.run(backfill())