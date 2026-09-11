from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.student import Student

from app.repositories.student_repository import (
    get_student_by_user_id as repository_get_student_by_user_id,
    get_student_classes as repository_get_student_classes,
    get_student_schedule as repository_get_student_schedule,
)


# ============================================================
# GET STUDENT PROFILE
# ============================================================

def get_student_by_user_id(
    db: Session,
    user_id: int,
) -> Student:

    student = repository_get_student_by_user_id(
        db=db,
        user_id=user_id,
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    return student


# ============================================================
# GET STUDENT CLASSES
# ============================================================

def get_student_classes(
    db: Session,
    user_id: int,
):

    # 1. Get student profile
    student = get_student_by_user_id(
        db=db,
        user_id=user_id,
    )

    # 2. Get classes through repository
    return repository_get_student_classes(
        db=db,
        student_id=student.studentID,
    )


# ============================================================
# GET STUDENT SCHEDULE
# ============================================================

def get_student_schedule(
    db: Session,
    user_id: int,
):

    # 1. Get student profile
    student = get_student_by_user_id(
        db=db,
        user_id=user_id,
    )

    # 2. Get schedule through repository
    return repository_get_student_schedule(
        db=db,
        student_id=student.studentID,
    )