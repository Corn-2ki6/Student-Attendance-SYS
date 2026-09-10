from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ClassSection(Base):
    __tablename__ = "class_sections"

    classID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    courseID: Mapped[int] = mapped_column(
        ForeignKey("courses.courseID"),
        nullable=False
    )

    lecturerID: Mapped[int] = mapped_column(
        ForeignKey("lecturers.lecturerID"),
        nullable=False
    )

    classCode: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    semester: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    academicYear: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )