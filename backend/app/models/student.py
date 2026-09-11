from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Student(Base):
    __tablename__ = "students"

    studentID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    userID: Mapped[int] = mapped_column(
        ForeignKey("users.userID"),
        nullable=False,
        unique=True
    )

    studentCode: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    fullName: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    dateOfBirth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    major: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )