from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_username(
    db: Session,
    username: str,
) -> User | None:
    result = db.execute(
        select(User).where(
            User.userName == username
        )
    )
    return result.scalar_one_or_none()


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    result = db.execute(
        select(User).where(
            User.userID == user_id
        )
    )
    return result.scalar_one_or_none()


def get_user_by_username_and_email(
    db: Session,
    username: str,
    email: str,
) -> User | None:
    result = db.execute(
        select(User).where(
            User.userName == username,
            User.email == email,
        )
    )
    return result.scalar_one_or_none()


def update_user_password(
    db: Session,
    user: User,
    password_hash: str,
) -> User:
    user.passwordHash = password_hash

    db.commit()
    db.refresh(user)

    return user