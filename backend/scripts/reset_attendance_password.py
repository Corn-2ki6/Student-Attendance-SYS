from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.attendance_session import AttendanceSession


db = SessionLocal()

try:
    result = db.execute(
        select(AttendanceSession).where(
            AttendanceSession.sessionID == 1
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        print("Session 1 not found")
    else:
        session.attendancePasswordHash = hash_password("123456")

        db.commit()

        print("Attendance password reset successfully.")
        print("Session ID:", session.sessionID)
        print("Password: 123456")

finally:
    db.close()