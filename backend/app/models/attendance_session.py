from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    sessionID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("class_sections.classID"),
        nullable=False
    )

    sessionDate: Mapped[date] = mapped_column(
        Date,
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

    attendanceMethod: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    attendancePasswordHash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="SCHEDULED"
    )