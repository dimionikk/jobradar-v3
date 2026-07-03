from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from anthropic import AsyncAnthropic
import json

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.vacancy import Vacancy
from app.schemas.ai import (
    CoverLetterRequest,
    CoverLetterResponse,
    MatchingResponse,
    MatchedVacancy,
)

router = APIRouter(prefix="/ai", tags=["AI"])
client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


@router.post("/cover-letter", response_model=CoverLetterResponse)
async def generate_cover_letter(
    request: CoverLetterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Vacancy).where(Vacancy.id == request.vacancy_id))
    vacancy = result.scalar_one_or_none()
    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )
    prompt = f"""Напиши супровідний лист українською мовою для відгуку на вакансію.
Дані кандидата:
- Стек технологій: {current_user.stack or "не вказано"}
- Досвід роботи: {current_user.experience_years or "не вказано"} років
- Про себе: {current_user.bio or "не вказано"}
Вакансія:
- Назва: {vacancy.title}
- Компанія: {vacancy.company}
- Опис: {vacancy.description}
Напиши короткий, конкретний, персоналізований супровідний лист (3-4 абзаци), без зайвих загальних фраз."""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    if not response.content:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service returned empty response",
        )

    return CoverLetterResponse(cover_letter=response.content[0].text)


@router.get("/matching", response_model=MatchingResponse)
async def get_matching_vacancies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Vacancy).where(Vacancy.is_active.is_(True))
    if current_user.city:
        query = query.where(Vacancy.city.ilike(f"%{current_user.city}%"))
    query = query.limit(20)

    result = await db.execute(query)
    vacancies = result.scalars().all()

    if not vacancies:
        return MatchingResponse(matches=[])

    vacancies_text = "\n\n".join(
        f"ID: {v.id}\nНазва: {v.title}\nКомпанія: {v.company}\nОпис: {v.description}"
        for v in vacancies
    )

    prompt = f"""Ось профіль кандидата:
Стек технологій: {current_user.stack or "не вказано"}
Досвід роботи: {current_user.experience_years or "не вказано"} років
Про себе: {current_user.bio or "не вказано"}
Ось список вакансій:
{vacancies_text}
Оціни наскільки кожна вакансія підходить кандидату за шкалою від 0 до 100 (match_score) і коротко поясни чому (reason).
Поверни ВІДПОВІДЬ ТІЛЬКИ у форматі валідного JSON-масиву, без жодного додаткового тексту до чи після, у точному форматі:
[{{"vacancy_id": 1, "match_score": 85, "reason": "..."}}]"""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    if not response.content:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service returned empty response",
        )

    raw_text = response.content[0].text.strip()


    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        ai_results = json.loads(raw_text)
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI service returned invalid JSON response",
        )

    vacancies_by_id = {v.id: v for v in vacancies}
    matches = []
    for item in ai_results:
        vacancy = vacancies_by_id.get(item.get("vacancy_id"))
        if vacancy is None:
            continue
        match_score = item.get("match_score")
        reason = item.get("reason")
        if match_score is None or reason is None:
            continue
        matches.append(MatchedVacancy(
            vacancy_id=vacancy.id,
            title=vacancy.title,
            company=vacancy.company,
            match_score=match_score,
            reason=reason,
        ))

    return MatchingResponse(matches=matches)