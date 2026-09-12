from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
    hash_password,
    decode_access_token,
)

from app.repositories.user_repository import (
    get_user_by_username,
    get_user_by_id,
    get_user_by_username_and_email,
    get_user_by_email,
    create_user,
    update_user_password,
)

from app.repositories.student_repository import (
    create_student,
)


# ============================================================
# REGISTER
# ============================================================

def register_user(
    db: Session,
    full_name: str,
    email: str,
    username: str,
    password: str,
):
    # 1. Check username
    existing_username = get_user_by_username(
        db=db,
        username=username,
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    # 2. Check email
    existing_email = get_user_by_email(
        db=db,
        email=email,
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    # 3. Validate password
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters",
        )

    # 4. Hash password
    password_hash = hash_password(password)

    try:
        # 5. Create User
        user = create_user(
            db=db,
            username=username,
            password_hash=password_hash,
            full_name=full_name,
            email=email,
        )

        # 6. Generate student code
        student_code = f"SV{user.userID:03d}"

        # 7. Create Student profile
        student = create_student(
            db=db,
            user_id=user.userID,
            student_code=student_code,
            full_name=full_name,
        )

        # 8. Commit User + Student
        db.commit()

        db.refresh(user)
        db.refresh(student)

        return {
            "userID": user.userID,
            "studentID": student.studentID,
            "username": user.userName,
            "fullName": user.fullName,
            "email": user.email,
            "studentCode": student.studentCode,
            "role": user.role,
            "status": user.status,
        }

    except Exception:
        db.rollback()
        raise


# ============================================================
# LOGIN
# ============================================================

def login_user(
    db: Session,
    username: str,
    password: str,
) -> str:

    # 1. Find user
    user = get_user_by_username(
        db=db,
        username=username,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # 2. Check account status
    if user.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    # 3. Verify password
    if not verify_password(
        password,
        user.passwordHash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # 4. Create JWT
    token_data = {
        "sub": str(user.userID),
        "role": user.role,
    }

    return create_access_token(token_data)


# ============================================================
# CHANGE PASSWORD
# ============================================================

def change_password(
    db: Session,
    user_id: int,
    current_password: str,
    new_password: str,
):

    # 1. Find user
    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # 2. Check current password
    if not verify_password(
        current_password,
        user.passwordHash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # 3. Validate new password
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters",
        )

    # 4. Prevent using the same password
    if verify_password(
        new_password,
        user.passwordHash,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    # 5. Hash new password
    new_password_hash = hash_password(
        new_password
    )

    # 6. Save through repository
    return update_user_password(
        db=db,
        user=user,
        password_hash=new_password_hash,
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

def forgot_password(
    db: Session,
    username: str,
    email: str,
):

    # 1. Find user by username + email
    user = get_user_by_username_and_email(
        db=db,
        username=username,
        email=email,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username or email is incorrect",
        )

    # 2. Generate reset token
    reset_token = create_access_token(
        {
            "sub": str(user.userID),
            "purpose": "PASSWORD_RESET",
        }
    )

    return reset_token


# ============================================================
# RESET PASSWORD
# ============================================================

def reset_password(
    db: Session,
    username: str,
    reset_token: str,
    new_password: str,
):

    # 1. Decode reset token
    try:
        payload = decode_access_token(
            reset_token
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired reset token",
        )

    # 2. Check token purpose
    if payload.get("purpose") != "PASSWORD_RESET":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid reset token",
        )

    user_id = payload.get("sub")

    # 3. Validate user ID
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid reset token",
        )

    # 4. Find user
    user = get_user_by_id(
        db=db,
        user_id=int(user_id),
    )

    if user is None or user.userName != username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # 5. Validate new password
    if len(new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be at least 6 characters",
        )

    # 6. Hash new password
    new_password_hash = hash_password(
        new_password
    )

    # 7. Save through repository
    return update_user_password(
        db=db,
        user=user,
        password_hash=new_password_hash,
    )