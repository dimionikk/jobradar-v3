from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, UniqueConstraint
from app.core.database import Base
from datetime import datetime

class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), nullable=False)
    status: Mapped[str] = mapped_column(default="applied")
    note: Mapped[str | None] = mapped_column()
    applied_at: Mapped[datetime] = mapped_column(server_default=func.now())
    vacancy: Mapped["Vacancy"] = relationship()

    __table_args__ = (
        UniqueConstraint("user_id", "vacancy_id", name="uq_user_application_vacancy"),
    )