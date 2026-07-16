import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.schemas.applications import ApplicationOut, ApplicationUpdate
from app.schemas.common import MessageResponse
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.vacancy import Vacancy
from app.models.applications import Application

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/{vacancy_id}", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def create_application(
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

    new_application = Application(user_id=current_user.id, vacancy_id=vacancy_id)
    db.add(new_application)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists for this vacancy",
        )

    return {"message": "Application created successfully"}


@router.get("/", response_model=list[ApplicationOut])
async def get_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.vacancy))
        .where(Application.user_id == current_user.id)
    )
    applications = result.scalars().all()
    return applications


@router.patch("/{application_id}", response_model=ApplicationOut)
async def update_application(
    application_id: int,
    request: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.vacancy))
        .where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    )
    application = result.scalar_one_or_none()
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)

    try:
        await db.commit()
    except (IntegrityError, DataError):
        await db.rollback()
        logger.exception("Failed to update application_id=%s", application_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update application with the provided data",
        )

    await db.refresh(application)
    return application


@router.delete("/{application_id}", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    )
    application = result.scalar_one_or_none()
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )
    await db.delete(application)
    await db.commit()
    return {"message": "Application deleted successfully"}