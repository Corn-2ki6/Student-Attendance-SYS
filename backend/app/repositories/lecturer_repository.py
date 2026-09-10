from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lecturer import Lecturer
from app.models.class_section import ClassSection
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.user import User
from app.models.attendance_session import AttendanceSession


def get_lecturer_by_user_id(
    db: Session,
    user_id: int,
) -> Lecturer | None:
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    return result.scalar_one_or_none()


def get_lecturer_classes(
    db: Session,
    lecturer_id: int,
):
    result = db.execute(
        select(
            ClassSection,
            Course,
        )
        .join(
            Course,
            ClassSection.courseID == Course.courseID,
        )
        .where(
            ClassSection.lecturerID == lecturer_id
        )
    )

    return result.all()


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


def get_class_students(
    db: Session,
    class_id: int,
):
    result = db.execute(
        select(
            Student,
            User,
            Enrollment,
        )
        .join(
            User,
            Student.userID == User.userID,
        )
        .join(
            Enrollment,
            Enrollment.studentID == Student.studentID,
        )
        .where(
            Enrollment.classID == class_id,
            Enrollment.status == "ACTIVE",
        )
        .order_by(
            Student.studentCode
        )
    )

    return result.all()


def get_lecturer_sessions(
    db: Session,
    lecturer_id: int,
    class_id: int | None = None,
    session_date=None,
    session_status: str | None = None,
):
    query = (
        select(
            AttendanceSession,
            ClassSection,
            Course,
        )
        .join(
            ClassSection,
            AttendanceSession.classID
            == ClassSection.classID,
        )
        .join(
            Course,
            ClassSection.courseID
            == Course.courseID,
        )
        .where(
            ClassSection.lecturerID == lecturer_id
        )
    )

    if class_id is not None:
        query = query.where(
            AttendanceSession.classID == class_id
        )

    if session_date is not None:
        query = query.where(
            AttendanceSession.sessionDate == session_date
        )

    if session_status is not None:
        query = query.where(
            AttendanceSession.status == session_status
        )

    query = query.order_by(
        AttendanceSession.sessionDate.desc(),
        AttendanceSession.startTime.desc(),
    )

    return db.execute(query).all()