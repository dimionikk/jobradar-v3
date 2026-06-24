from app.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    stack: Mapped[str | None] = mapped_column()
    experience_years: Mapped[int | None] = mapped_column()
    salary_expectation: Mapped[int | None] = mapped_column()
    city: Mapped[str | None] = mapped_column()
    work_type: Mapped[str | None] = mapped_column()
    bio: Mapped[str | None] = mapped_column()
    resume_text: Mapped[str | None] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())