from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.models.enrollment import Enrollment
from app.models.class_section import ClassSection
from app.models.course import Course
from app.models.schedule import Schedule
from app.models.attendance_record import AttendanceRecord
from app.models.attendance_session import AttendanceSession


def get_student_by_user_id(
    db: Session,
    user_id: int,
) -> Student | None:
    result = db.execute(
        select(Student).where(
            Student.userID == user_id
        )
    )
    return result.scalar_one_or_none()


def get_student_classes(
    db: Session,
    student_id: int,
):
    result = db.execute(
        select(
            Enrollment,
            ClassSection,
            Course,
        )
        .join(
            ClassSection,
            Enrollment.classID == ClassSection.classID,
        )
        .join(
            Course,
            ClassSection.courseID == Course.courseID,
        )
        .where(
            Enrollment.studentID == student_id,
            Enrollment.status == "ACTIVE",
        )
    )

    return result.all()


def get_student_schedule(
    db: Session,
    student_id: int,
):
    result = db.execute(
        select(
            Schedule,
            ClassSection,
            Course,
        )
        .join(
            ClassSection,
            Schedule.classID == ClassSection.classID,
        )
        .join(
            Course,
            ClassSection.courseID == Course.courseID,
        )
        .join(
            Enrollment,
            Enrollment.classID == ClassSection.classID,
        )
        .where(
            Enrollment.studentID == student_id,
            Enrollment.status == "ACTIVE",
        )
    )

    return result.all()


def get_student_attendance_records(
    db: Session,
    student_id: int,
):
    result = db.execute(
        select(AttendanceRecord)
        .where(
            AttendanceRecord.studentID == student_id
        )
    )

    return result.scalars().all()


def get_student_attendance_history(
    db: Session,
    student_id: int,
):
    result = db.execute(
        select(
            AttendanceRecord,
            AttendanceSession,
        )
        .join(
            AttendanceSession,
            AttendanceRecord.sessionID
            == AttendanceSession.sessionID,
        )
        .where(
            AttendanceRecord.studentID == student_id
        )
        .order_by(
            AttendanceSession.sessionDate.desc(),
            AttendanceSession.startTime.desc(),
        )
    )

    return result.all()

def create_student(
    db: Session,
    user_id: int,
    student_code: str,
    full_name: str,
) -> Student:

    student = Student(
        userID=user_id,
        studentCode=student_code,
        fullName=full_name,
    )

    db.add(student)

    return student