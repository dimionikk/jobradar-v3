from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey, func
from app.core.database import Base
from datetime import datetime


class SavedVacancy(Base):
    __tablename__ = "saved_vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(server_default=func.now())