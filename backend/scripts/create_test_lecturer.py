from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User
from app.models.lecturer import Lecturer


USERNAME = "lecturer01"
PASSWORD = "123456"


def create_test_lecturer():
    db = SessionLocal()

    try:
        user = db.execute(
            select(User).where(User.userName == USERNAME)
        ).scalar_one_or_none()

        if user is None:
            user = User(
                userName=USERNAME,
                passwordHash=hash_password(PASSWORD),
                fullName="Test Lecturer",
                email="lecturer01@example.com",
                status="ACTIVE",
                role="LECTURER",
            )

            db.add(user)
            db.flush()

            print("Lecturer user created.")

        else:
            print(f"User '{USERNAME}' already exists.")

        existing_lecturer = db.execute(
            select(Lecturer).where(Lecturer.userID == user.userID)
        ).scalar_one_or_none()

        if existing_lecturer:
            print("Lecturer record already exists.")
            print(f"Lecturer ID: {existing_lecturer.lecturerID}")
            return

        lecturer = Lecturer(
            userID=user.userID,
            lecturerCode="GV001",
            fullName="Test Lecturer",
            department="International Relations",
        )

        db.add(lecturer)
        db.commit()
        db.refresh(lecturer)

        print("Test lecturer created successfully!")
        print(f"Lecturer ID: {lecturer.lecturerID}")
        print(f"Lecturer Code: {lecturer.lecturerCode}")
        print(f"User ID: {lecturer.userID}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_lecturer()