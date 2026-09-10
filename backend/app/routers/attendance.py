from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role

from app.schemas.attendance import (
    AttendanceSubmitRequest,
    AttendanceSessionCreateRequest,
    AttendanceRecordUpdateRequest,
    AttendanceReportResponse,
)

from app.services.attendance_service import (
    create_attendance_session,
    open_attendance_session,
    submit_attendance,
    get_student_attendance_history,
    get_student_attendance_percentage,
    close_attendance_session,
    get_session_attendance_records,
    update_attendance_record,
    get_attendance_report,
)


router = APIRouter(
    prefix="/api/attendance",
    tags=["Attendance"],
)


# ============================================================
# CREATE ATTENDANCE SESSION - LECTURER
# ============================================================

@router.post("/sessions")
def create_session(
    request: AttendanceSessionCreateRequest,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    session = create_attendance_session(
        db=db,
        user_id=int(current_user["user_id"]),
        class_id=request.classID,
        session_date=request.sessionDate,
        start_time=request.startTime,
        end_time=request.endTime,
        attendance_method=request.attendanceMethod,
        attendance_password=request.attendancePassword,
    )

    return {
        "sessionID": session.sessionID,
        "classID": session.classID,
        "sessionDate": session.sessionDate,
        "startTime": session.startTime,
        "endTime": session.endTime,
        "attendanceMethod": session.attendanceMethod,
        "status": session.status,
    }


# ============================================================
# OPEN ATTENDANCE SESSION - LECTURER
# ============================================================

@router.post("/sessions/{session_id}/open")
def open_session(
    session_id: int,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    session = open_attendance_session(
        db=db,
        session_id=session_id,
        user_id=int(current_user["user_id"]),
    )

    return {
        "sessionID": session.sessionID,
        "classID": session.classID,
        "sessionDate": session.sessionDate,
        "startTime": session.startTime,
        "endTime": session.endTime,
        "attendanceMethod": session.attendanceMethod,
        "status": session.status,
    }


# ============================================================
# STUDENT SUBMIT ATTENDANCE
# ============================================================

@router.post("/sessions/{session_id}/submit")
def submit_session_attendance(
    session_id: int,
    request: AttendanceSubmitRequest,
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    attendance = submit_attendance(
        db=db,
        session_id=session_id,
        user_id=int(current_user["user_id"]),
        password=request.password,
    )

    return {
        "attendanceID": attendance.attendanceID,
        "sessionID": attendance.sessionID,
        "studentID": attendance.studentID,
        "status": attendance.status,
        "checkInTime": attendance.checkInTime,
        "method": attendance.method,
        "remark": attendance.remark,
    }


# ============================================================
# STUDENT ATTENDANCE HISTORY
# ============================================================

@router.get("/me/history")
def get_my_attendance_history(
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    results = get_student_attendance_history(
        db=db,
        user_id=int(current_user["user_id"]),
    )

    return [
        {
            "attendanceID": attendance.attendanceID,
            "sessionID": session.sessionID,
            "classID": session.classID,
            "sessionDate": session.sessionDate,
            "startTime": session.startTime,
            "endTime": session.endTime,
            "attendanceMethod": session.attendanceMethod,
            "status": attendance.status,
            "checkInTime": attendance.checkInTime,
            "method": attendance.method,
            "remark": attendance.remark,
        }
        for attendance, session in results
    ]


# ============================================================
# STUDENT ATTENDANCE PERCENTAGE
# ============================================================

@router.get("/me/percentage")
def get_my_attendance_percentage(
    current_user: dict = Depends(require_role("STUDENT")),
    db: Session = Depends(get_db),
):
    return get_student_attendance_percentage(
        db=db,
        user_id=int(current_user["user_id"]),
    )


# ============================================================
# CLOSE ATTENDANCE SESSION - LECTURER
# ============================================================

@router.post("/sessions/{session_id}/close")
def close_session(
    session_id: int,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    session = close_attendance_session(
        db=db,
        session_id=session_id,
        user_id=int(current_user["user_id"]),
    )

    return {
        "sessionID": session.sessionID,
        "classID": session.classID,
        "sessionDate": session.sessionDate,
        "startTime": session.startTime,
        "endTime": session.endTime,
        "attendanceMethod": session.attendanceMethod,
        "status": session.status,
    }

# ============================================================
# GET ATTENDANCE RECORDS - LECTURER
# ============================================================

@router.get("/sessions/{session_id}/records")
def get_attendance_records(
    session_id: int,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    results = get_session_attendance_records(
        db=db,
        session_id=session_id,
        user_id=int(current_user["user_id"]),
    )

    return [
        {
            "attendanceID": attendance.attendanceID,
            "studentID": student.studentID,
            "studentCode": student.studentCode,
            "fullName": student.fullName,
            "status": attendance.status,
            "checkInTime": attendance.checkInTime,
            "method": attendance.method,
            "remark": attendance.remark,
        }
        for attendance, student in results
    ]

# ============================================================
# UPDATE ATTENDANCE RECORD - LECTURER
# ============================================================

@router.put("/records/{attendance_id}")
def update_record(
    attendance_id: int,
    request: AttendanceRecordUpdateRequest,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    attendance = update_attendance_record(
        db=db,
        attendance_id=attendance_id,
        user_id=int(current_user["user_id"]),
        new_status=request.status,
        remark=request.remark,
    )

    return {
        "attendanceID": attendance.attendanceID,
        "sessionID": attendance.sessionID,
        "studentID": attendance.studentID,
        "status": attendance.status,
        "checkInTime": attendance.checkInTime,
        "method": attendance.method,
        "remark": attendance.remark,
    }

# ============================================================
# ATTENDANCE REPORT - LECTURER
# ============================================================

@router.get(
    "/sessions/{session_id}/report",
    response_model=AttendanceReportResponse,
)
def get_session_report(
    session_id: int,
    current_user: dict = Depends(require_role("LECTURER")),
    db: Session = Depends(get_db),
):
    return get_attendance_report(
        db=db,
        session_id=session_id,
        user_id=int(current_user["user_id"]),
    )