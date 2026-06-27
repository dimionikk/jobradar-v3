from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.models.saved_vacancy import SavedVacancy

router = APIRouter(prefix="/saved-vacancies", tags=["Saved Vacancies"])


@router.post("/{vacancy_id}", status_code=status.HTTP_201_CREATED)
async def save_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    vacancy_result = await db.execute(select(Vacancy).where(Vacancy.id == vacancy_id))
    vacancy = vacancy_result.scalar_one_or_none()

    if vacancy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacancy not found",
        )

    existing_result = await db.execute(
        select(SavedVacancy).where(
            SavedVacancy.user_id == current_user.id,
            SavedVacancy.vacancy_id == vacancy_id,
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vacancy already saved",
        )

    new_saved = SavedVacancy(user_id=current_user.id, vacancy_id=vacancy_id)
    db.add(new_saved)
    await db.commit()

    return {"message": "Vacancy saved successfully"}

from app.schemas.vacancy import VacancyOut

@router.get("/", response_model=list[VacancyOut])
async def get_saved_vacancies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Vacancy)
        .join(SavedVacancy, SavedVacancy.vacancy_id == Vacancy.id)
        .where(SavedVacancy.user_id == current_user.id)
    )
    vacancies = result.scalars().all()
    return vacancies

@router.delete("/{vacancy_id}")
async def remove_saved_vacancy(
    vacancy_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(SavedVacancy).where(
            SavedVacancy.vacancy_id == vacancy_id,
            SavedVacancy.user_id == current_user.id,
        )
    )
    saved = result.scalar_one_or_none()

    if saved is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Saved vacancy not found",
        )

    await db.delete(saved)
    await db.commit()

    return {"message": "Vacancy removed from saved"}