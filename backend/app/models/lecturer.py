from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturerID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    userID: Mapped[int] = mapped_column(
        ForeignKey("users.userID"),
        nullable=False,
        unique=True
    )

    lecturerCode: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    fullName: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )