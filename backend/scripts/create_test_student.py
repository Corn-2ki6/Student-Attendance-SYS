from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.student import Student
from app.models.user import User


def create_test_student():
    db = SessionLocal()

    try:
        user = db.execute(
            select(User).where(User.userName == "student01")
        ).scalar_one_or_none()

        if user is None:
            print("User 'student01' does not exist.")
            return

        existing_student = db.execute(
            select(Student).where(Student.userID == user.userID)
        ).scalar_one_or_none()

        if existing_student:
            print("Student record already exists.")
            print(f"Student ID: {existing_student.studentID}")
            return

        student = Student(
            userID=user.userID,
            studentCode="SV001",
            fullName="Test Student",
            major="International Relations",
        )

        db.add(student)
        db.commit()
        db.refresh(student)

        print("Test student created successfully!")
        print(f"Student ID: {student.studentID}")
        print(f"Student Code: {student.studentCode}")
        print(f"User ID: {student.userID}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_student()