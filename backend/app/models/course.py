from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    courseID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    courseCode: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    courseName: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    credits: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )