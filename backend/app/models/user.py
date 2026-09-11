from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    userID: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    userName: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    passwordHash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    fullName: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="ACTIVE"
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="STUDENT"
    )