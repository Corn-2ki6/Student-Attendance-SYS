from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


USERNAME = "student01"
PASSWORD = "123456"


def create_test_user():
    db = SessionLocal()

    try:
        existing_user = db.execute(
            select(User).where(User.userName == USERNAME)
        ).scalar_one_or_none()

        if existing_user:
            print(f"User '{USERNAME}' already exists.")
            return

        user = User(
            userName=USERNAME,
            passwordHash=hash_password(PASSWORD),
            fullName="Test Student",
            email="student01@example.com",
            status="ACTIVE",
            role="STUDENT",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print("Test user created successfully!")
        print(f"User ID: {user.userID}")
        print(f"Username: {user.userName}")
        print(f"Role: {user.role}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_user()