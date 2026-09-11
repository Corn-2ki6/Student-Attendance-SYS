from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.lecturer import Lecturer

from app.repositories.lecturer_repository import (
    get_lecturer_by_user_id as repository_get_lecturer_by_user_id,
    get_lecturer_classes as repository_get_lecturer_classes,
    get_class_by_lecturer,
    get_class_students as repository_get_class_students,
    get_lecturer_sessions as repository_get_lecturer_sessions,
)


# ============================================================
# GET LECTURER PROFILE
# ============================================================

def get_lecturer_by_user_id(
    db: Session,
    user_id: int,
) -> Lecturer:

    lecturer = repository_get_lecturer_by_user_id(
        db=db,
        user_id=user_id,
    )

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    return lecturer


# ============================================================
# GET LECTURER CLASSES
# ============================================================

def get_lecturer_classes(
    db: Session,
    user_id: int,
):

    # 1. Get lecturer profile
    lecturer = get_lecturer_by_user_id(
        db=db,
        user_id=user_id,
    )

    # 2. Get classes through repository
    return repository_get_lecturer_classes(
        db=db,
        lecturer_id=lecturer.lecturerID,
    )


# ============================================================
# GET STUDENTS IN CLASS
# ============================================================

def get_class_students(
    db: Session,
    user_id: int,
    class_id: int,
):

    # 1. Get lecturer profile
    lecturer = get_lecturer_by_user_id(
        db=db,
        user_id=user_id,
    )

    # 2. Check lecturer owns this class
    class_section = get_class_by_lecturer(
        db=db,
        class_id=class_id,
        lecturer_id=lecturer.lecturerID,
    )

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 3. Get students through repository
    return repository_get_class_students(
        db=db,
        class_id=class_id,
    )


# ============================================================
# GET LECTURER ATTENDANCE SESSIONS
# ============================================================

def get_lecturer_sessions(
    db: Session,
    user_id: int,
    class_id: int | None = None,
    session_date=None,
    session_status: str | None = None,
):

    # 1. Get lecturer profile
    lecturer = get_lecturer_by_user_id(
        db=db,
        user_id=user_id,
    )

    # 2. Validate session status
    if session_status is not None:

        allowed_statuses = [
            "SCHEDULED",
            "OPEN",
            "CLOSED",
        ]

        if session_status not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid session status",
            )

    # 3. Get sessions through repository
    return repository_get_lecturer_sessions(
        db=db,
        lecturer_id=lecturer.lecturerID,
        class_id=class_id,
        session_date=session_date,
        session_status=session_status,
    )