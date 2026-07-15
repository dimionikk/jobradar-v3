import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import redis_client
from app.schemas.user import UserOut, UserUpdate
from app.core.dependencies import get_current_user
from app.schemas.common import MessageResponse
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get("/", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/", response_model=UserOut)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        logger.exception("Failed to update profile for user_id=%s", current_user.id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update profile with the provided data",
        )

    await db.refresh(current_user)

    try:
        await redis_client.delete(f"matching:{current_user.id}")
    except Exception:
        logger.exception("Failed to invalidate matching cache for user_id=%s", current_user.id)

    return current_user


@router.delete("/", response_model=MessageResponse)
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    current_user.is_active = False
    await db.commit()
    return {"message": "Profile deactivated successfully"}