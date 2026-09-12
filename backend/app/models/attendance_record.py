from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    __table_args__ = (
        UniqueConstraint(
            "sessionID",
            "studentID",
            name="uq_attendance_session_student"
        ),
    )

    attendanceID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    sessionID: Mapped[int] = mapped_column(
        ForeignKey("attendance_sessions.sessionID"),
        nullable=False
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("students.studentID"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    checkInTime: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    method: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    remark: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )