from datetime import datetime

from sqlalchemy import ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SavedVacancy(Base):
    __tablename__ = "saved_vacancies"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False)
    saved_at: Mapped[datetime] = mapped_column(server_default=func.now())

    vacancy: Mapped["Vacancy"] = relationship(lazy="selectin")

    __table_args__ = (
        UniqueConstraint("user_id", "vacancy_id", name="uq_user_saved_vacancy"),
    )