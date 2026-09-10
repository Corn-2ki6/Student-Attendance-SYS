from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendance_session import AttendanceSession
from app.models.attendance_record import AttendanceRecord
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.lecturer import Lecturer
from app.models.class_section import ClassSection


# ============================================================
# ATTENDANCE SESSION
# ============================================================

def get_session_by_id(
    db: Session,
    session_id: int,
) -> AttendanceSession | None:

    result = db.execute(
        select(AttendanceSession).where(
            AttendanceSession.sessionID == session_id
        )
    )

    return result.scalar_one_or_none()


def get_overlapping_session(
    db: Session,
    class_id: int,
    session_date,
    start_time,
    end_time,
):
    """
    Find an existing session that overlaps
    with the requested time.
    """

    result = db.execute(
        select(AttendanceSession).where(
            AttendanceSession.classID == class_id,
            AttendanceSession.sessionDate == session_date,
            AttendanceSession.startTime < end_time,
            AttendanceSession.endTime > start_time,
        )
    )

    return result.scalar_one_or_none()


def add_session(
    db: Session,
    attendance_session: AttendanceSession,
):
    db.add(attendance_session)


# ============================================================
# LECTURER
# ============================================================

def get_lecturer_by_user_id(
    db: Session,
    user_id: int,
):
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    return result.scalar_one_or_none()


def get_class_by_lecturer(
    db: Session,
    class_id: int,
    lecturer_id: int,
):
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == class_id,
            ClassSection.lecturerID == lecturer_id,
        )
    )

    return result.scalar_one_or_none()


# ============================================================
# STUDENT
# ============================================================

def get_student_by_user_id(
    db: Session,
    user_id: int,
):
    result = db.execute(
        select(Student).where(
            Student.userID == user_id
        )
    )

    return result.scalar_one_or_none()


def get_enrollment(
    db: Session,
    student_id: int,
    class_id: int,
):
    result = db.execute(
        select(Enrollment).where(
            Enrollment.studentID == student_id,
            Enrollment.classID == class_id,
            Enrollment.status == "ACTIVE",
        )
    )

    return result.scalar_one_or_none()


def get_enrolled_students(
    db: Session,
    class_id: int,
):
    result = db.execute(
        select(
            Enrollment,
            Student,
        )
        .join(
            Student,
            Enrollment.studentID == Student.studentID,
        )
        .where(
            Enrollment.classID == class_id,
            Enrollment.status == "ACTIVE",
        )
    )

    return result.all()


# ============================================================
# ATTENDANCE RECORD
# ============================================================

def get_attendance_record(
    db: Session,
    session_id: int,
    student_id: int,
):
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.sessionID == session_id,
            AttendanceRecord.studentID == student_id,
        )
    )

    return result.scalar_one_or_none()


def get_attendance_record_by_id(
    db: Session,
    attendance_id: int,
):
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.attendanceID == attendance_id
        )
    )

    return result.scalar_one_or_none()


def get_session_records(
    db: Session,
    session_id: int,
):
    result = db.execute(
        select(
            AttendanceRecord,
            Student,
        )
        .join(
            Student,
            AttendanceRecord.studentID == Student.studentID,
        )
        .where(
            AttendanceRecord.sessionID == session_id
        )
        .order_by(
            Student.studentCode
        )
    )

    return result.all()


def get_all_session_records(
    db: Session,
    session_id: int,
):
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.sessionID == session_id
        )
    )

    return result.scalars().all()


def add_attendance_record(
    db: Session,
    attendance_record: AttendanceRecord,
):
    db.add(attendance_record)


# ============================================================
# DATABASE OPERATIONS
# ============================================================

def flush(db: Session):
    db.flush()


def commit(db: Session):
    db.commit()


def refresh(
    db: Session,
    obj,
):
    db.refresh(obj)