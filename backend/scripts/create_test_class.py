from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.class_section import ClassSection
from app.models.course import Course
from app.models.lecturer import Lecturer


def create_test_class():
    db = SessionLocal()

    try:
        course = db.execute(
            select(Course).where(Course.courseCode == "IR101")
        ).scalar_one_or_none()

        if course is None:
            print("Course 'IR101' does not exist.")
            return

        lecturer = db.execute(
            select(Lecturer).where(Lecturer.lecturerCode == "GV001")
        ).scalar_one_or_none()

        if lecturer is None:
            print("Lecturer 'GV001' does not exist.")
            return

        existing_class = db.execute(
            select(ClassSection).where(
                ClassSection.classCode == "IR101-01"
            )
        ).scalar_one_or_none()

        if existing_class:
            print("Class section already exists.")
            print(f"Class ID: {existing_class.classID}")
            return

        class_section = ClassSection(
            courseID=course.courseID,
            lecturerID=lecturer.lecturerID,
            classCode="IR101-01",
            semester="Semester 1",
            academicYear="2026-2027",
        )

        db.add(class_section)
        db.commit()
        db.refresh(class_section)

        print("Test class section created successfully!")
        print(f"Class ID: {class_section.classID}")
        print(f"Class Code: {class_section.classCode}")
        print(f"Course ID: {class_section.courseID}")
        print(f"Lecturer ID: {class_section.lecturerID}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_class()