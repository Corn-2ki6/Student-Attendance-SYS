from datetime import time

from sqlalchemy import ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    scheduleID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("class_sections.classID"),
        nullable=False
    )

    dayOfWeek: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    startTime: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    endTime: Mapped[time] = mapped_column(
        Time,
        nullable=False
    )

    room: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )