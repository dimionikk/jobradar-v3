from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, verify_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.core.dependencies import oauth2_scheme
from app.core.redis_client import redis_client
from datetime import datetime, timezone

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User).where(User.email == user.email))
    existing_user = results.scalar_one_or_none()
    if existing_user: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User).where(User.email == user.email))
    existing_user = results.scalar_one_or_none()
    if not existing_user or not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": existing_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    ttl = exp - int(datetime.now(timezone.utc).timestamp())
    if ttl > 0:
        await redis_client.set(token, "blacklisted", ex=ttl)
    
    return {"message": "Logged out successfully"}