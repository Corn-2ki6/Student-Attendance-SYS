from datetime import date, time

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.attendance_session import AttendanceSession
from app.models.class_section import ClassSection


def create_test_attendance_session():
    db = SessionLocal()

    try:
        class_section = db.execute(
            select(ClassSection).where(
                ClassSection.classCode == "IR101-01"
            )
        ).scalar_one_or_none()

        if class_section is None:
            print("Class 'IR101-01' does not exist.")
            return

        existing_session = db.execute(
            select(AttendanceSession).where(
                AttendanceSession.classID == class_section.classID,
                AttendanceSession.sessionDate == date.today(),
            )
        ).scalar_one_or_none()

        if existing_session:
            print("Attendance session already exists.")
            print(f"Session ID: {existing_session.sessionID}")
            return

        session = AttendanceSession(
            classID=class_section.classID,
            sessionDate=date.today(),
            startTime=time(8, 0),
            endTime=time(10, 0),
            attendanceMethod="PASSWORD",
            attendancePasswordHash=hash_password("123456"),
            status="SCHEDULED",
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        print("Test attendance session created successfully!")
        print(f"Session ID: {session.sessionID}")
        print(f"Class ID: {session.classID}")
        print(f"Date: {session.sessionDate}")
        print(f"Time: {session.startTime} - {session.endTime}")
        print(f"Method: {session.attendanceMethod}")
        print(f"Status: {session.status}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_attendance_session()