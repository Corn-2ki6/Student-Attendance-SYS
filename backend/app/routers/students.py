from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import ChangePasswordRequest
from app.services.auth_service import change_password

from app.core.database import get_db
from app.core.dependencies import require_role
from app.services.student_service import (
    get_student_by_user_id,
    get_student_classes,
    get_student_schedule,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Students"],
)


@router.get("/me")
def get_my_profile(
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    student = get_student_by_user_id(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return {
        "studentID": student.studentID,
        "studentCode": student.studentCode,
        "fullName": student.fullName,
        "dateOfBirth": student.dateOfBirth,
        "gender": student.gender,
        "major": student.major,
    }


@router.get("/me/classes")
def get_my_classes(
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    results = get_student_classes(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return [
        {
            "enrollmentID": enrollment.enrollmentID,
            "classID": class_section.classID,
            "classCode": class_section.classCode,
            "semester": class_section.semester,
            "academicYear": class_section.academicYear,
            "courseID": course.courseID,
            "courseCode": course.courseCode,
            "courseName": course.courseName,
            "credits": course.credits,
        }
        for enrollment, class_section, course in results
    ]


@router.get("/me/schedule")
def get_my_schedule(
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    results = get_student_schedule(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return [
        {
            "scheduleID": schedule.scheduleID,
            "classID": class_section.classID,
            "classCode": class_section.classCode,
            "courseCode": course.courseCode,
            "courseName": course.courseName,
            "dayOfWeek": schedule.dayOfWeek,
            "startTime": schedule.startTime,
            "endTime": schedule.endTime,
            "room": schedule.room,
        }
        for schedule, class_section, course in results
    ]

@router.put("/me/password")
def change_my_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(require_role("STUDENT")),
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