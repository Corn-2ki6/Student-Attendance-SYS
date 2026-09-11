from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.course import Course


def create_test_course():
    db = SessionLocal()

    try:
        existing_course = db.execute(
            select(Course).where(Course.courseCode == "IR101")
        ).scalar_one_or_none()

        if existing_course:
            print("Course already exists.")
            print(f"Course ID: {existing_course.courseID}")
            return

        course = Course(
            courseCode="IR101",
            courseName="Introduction to International Relations",
            credits=3,
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        print("Test course created successfully!")
        print(f"Course ID: {course.courseID}")
        print(f"Course Code: {course.courseCode}")
        print(f"Course Name: {course.courseName}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_course()