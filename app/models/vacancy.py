from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import func, String, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    company: Mapped[str | None] = mapped_column(String(300))
    city: Mapped[str | None] = mapped_column(String(100))
    salary: Mapped[str | None] = mapped_column(String(100))
    work_type: Mapped[str | None] = mapped_column(String(50))
    experience: Mapped[str | None] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    parsed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1024), nullable=True)

    __table_args__ = (
        Index("ix_vacancies_active_source", "is_active", "source"),
    )