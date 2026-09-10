from datetime import date

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.student import Student
from app.models.class_section import ClassSection
from app.models.enrollment import Enrollment


def create_test_enrollment():
    db = SessionLocal()

    try:
        student = db.execute(
            select(Student).where(Student.studentCode == "SV001")
        ).scalar_one_or_none()

        if student is None:
            print("Student 'SV001' does not exist.")
            return

        class_section = db.execute(
            select(ClassSection).where(
                ClassSection.classCode == "IR101-01"
            )
        ).scalar_one_or_none()

        if class_section is None:
            print("Class 'IR101-01' does not exist.")
            return

        existing_enrollment = db.execute(
            select(Enrollment).where(
                Enrollment.studentID == student.studentID,
                Enrollment.classID == class_section.classID,
            )
        ).scalar_one_or_none()

        if existing_enrollment:
            print("Enrollment already exists.")
            print(f"Enrollment ID: {existing_enrollment.enrollmentID}")
            return

        enrollment = Enrollment(
            studentID=student.studentID,
            classID=class_section.classID,
            enrollmentDate=date.today(),
            status="ACTIVE",
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)

        print("Test enrollment created successfully!")
        print(f"Enrollment ID: {enrollment.enrollmentID}")
        print(f"Student ID: {enrollment.studentID}")
        print(f"Class ID: {enrollment.classID}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_enrollment()