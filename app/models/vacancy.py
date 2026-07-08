from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from sqlalchemy import func
from datetime import datetime
from pgvector.sqlalchemy import Vector


class Vacancy(Base):
    __tablename__ = "vacancies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column()
    company: Mapped[str | None] = mapped_column()
    city: Mapped[str | None] = mapped_column()
    salary: Mapped[str | None] = mapped_column()
    work_type: Mapped[str | None] = mapped_column()
    experience: Mapped[str | None] = mapped_column()
    url: Mapped[str] = mapped_column(unique=True, nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    parsed_at: Mapped[datetime] = mapped_column(server_default=func.now())
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1024), nullable=True)