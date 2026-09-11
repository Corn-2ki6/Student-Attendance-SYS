from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role
from app.schemas.auth import ChangePasswordRequest
from app.services.auth_service import change_password

from app.services.lecturer_service import (
    get_lecturer_by_user_id,
    get_lecturer_classes,
    get_class_students,
    get_lecturer_sessions,
)


router = APIRouter(
    prefix="/api/lecturers",
    tags=["Lecturers"],
)


# ============================================================
# GET LECTURER PROFILE
# ============================================================

@router.get("/me")
def get_my_profile(
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    lecturer = get_lecturer_by_user_id(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return {
        "lecturerID": lecturer.lecturerID,
        "lecturerCode": lecturer.lecturerCode,
        "fullName": lecturer.fullName,
        "department": lecturer.department,
    }


# ============================================================
# GET LECTURER CLASSES
# ============================================================

@router.get("/me/classes")
def get_my_classes(
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    results = get_lecturer_classes(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return [
        {
            "classID": class_section.classID,
            "classCode": class_section.classCode,
            "semester": class_section.semester,
            "academicYear": class_section.academicYear,
            "courseID": course.courseID,
            "courseCode": course.courseCode,
            "courseName": course.courseName,
            "credits": course.credits,
        }
        for class_section, course in results
    ]


# ============================================================
# GET STUDENTS IN CLASS
# ============================================================

@router.get("/classes/{class_id}/students")
def get_students_in_class(
    class_id: int,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    results = get_class_students(
        db=db,
        user_id=int(current_user["user_id"]),
        class_id=class_id,
    )

    return [
        {
            "studentID": student.studentID,
            "studentCode": student.studentCode,
            "fullName": student.fullName,
            "email": user.email,
            "enrollmentID": enrollment.enrollmentID,
            "enrollmentStatus": enrollment.status,
        }
        for student, user, enrollment in results
    ]


# ============================================================
# GET LECTURER ATTENDANCE SESSIONS
# ============================================================

@router.get("/me/sessions")
def get_my_sessions(
    class_id: int | None = None,
    session_date: date | None = None,
    status: str | None = None,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    results = get_lecturer_sessions(
        db=db,
        user_id=int(current_user["user_id"]),
        class_id=class_id,
        session_date=session_date,
        session_status=status,
    )

    return [
        {
            "sessionID": session.sessionID,
            "classID": class_section.classID,
            "classCode": class_section.classCode,
            "courseCode": course.courseCode,
            "courseName": course.courseName,
            "sessionDate": session.sessionDate,
            "startTime": session.startTime,
            "endTime": session.endTime,
            "attendanceMethod": session.attendanceMethod,
            "status": session.status,
        }
        for session, class_section, course in results
    ]

# ============================================================
# CHANGE LECTURER PASSWORD
# ============================================================

@router.put("/me/password")
def change_lecturer_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    change_password(
        db=db,
        user_id=int(current_user["user_id"]),
        current_password=request.currentPassword,
        new_password=request.newPassword,
    )

    return {
        "message": "Password changed successfully"
    }