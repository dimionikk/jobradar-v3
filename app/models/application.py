from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
from app.core.database import Base
from datetime import datetime


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"))
    status: Mapped[str] = mapped_column(default="applied")
    note: Mapped[str | None] = mapped_column()
    applied_at: Mapped[datetime] = mapped_column(server_default=func.now())