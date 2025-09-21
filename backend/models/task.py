from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class TaskStatus(StrEnum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TaskStatus]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title})"
