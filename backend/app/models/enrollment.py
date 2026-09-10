from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollmentID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    studentID: Mapped[int] = mapped_column(
        ForeignKey("students.studentID"),
        nullable=False
    )

    classID: Mapped[int] = mapped_column(
        ForeignKey("class_sections.classID"),
        nullable=False
    )

    enrollmentDate: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )