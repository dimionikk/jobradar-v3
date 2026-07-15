from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    stack: Mapped[str | None] = mapped_column(String(500))
    experience_years: Mapped[int | None] = mapped_column()
    salary_expectation: Mapped[int | None] = mapped_column()
    city: Mapped[str | None] = mapped_column(String(100))
    work_type: Mapped[str | None] = mapped_column(String(50))
    bio: Mapped[str | None] = mapped_column(String(2000))
    resume_text: Mapped[str | None] = mapped_column(String(10000))

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())