from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserOut, UserUpdate
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get("/", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)) -> UserOut:
    return current_user


@router.patch("/", response_model=UserOut)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/", response_model=dict)
async def delete_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.delete(current_user)
    await db.commit()
    return {"message": "Profile deleted successfully"}