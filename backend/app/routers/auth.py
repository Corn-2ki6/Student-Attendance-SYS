from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user

from app.schemas.auth import (
    TokenResponse,
    RegisterRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.services.auth_service import (
    login_user,
    register_user,
    forgot_password,
    reset_password,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    result = register_user(
        db=db,
        full_name=request.fullName,
        email=request.email,
        username=request.username,
        password=request.password,
    )

    return {
        "message": "Registration completed successfully",
        "user": result,
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    access_token = login_user(
        db=db,
        username=form_data.username,
        password=form_data.password,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


# ============================================================
# GET CURRENT USER
# ============================================================

@router.get("/me")
def get_me(
    current_user: dict = Depends(get_current_user),
):
    return current_user


# ============================================================
# FORGOT PASSWORD
# ============================================================

@router.post("/forgot-password")
def forgot_password_endpoint(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    reset_token = forgot_password(
        db=db,
        username=request.username,
        email=request.email,
    )

    return {
        "message": "Reset token generated successfully",
        "reset_token": reset_token,
    }


# ============================================================
# RESET PASSWORD
# ============================================================

@router.post("/reset-password")
def reset_password_endpoint(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    reset_password(
        db=db,
        username=request.username,
        reset_token=request.reset_token,
        new_password=request.newPassword,
    )

    return {
        "message": "Password reset successfully"
    }


# ============================================================
# LOGOUT
# ============================================================

@router.post("/logout")
def logout(
    current_user: dict = Depends(get_current_user),
):
    return {
        "message": "Logout successful"
    }