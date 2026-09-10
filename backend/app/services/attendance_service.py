from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password, hash_password

from app.models.attendance_session import AttendanceSession
from app.models.attendance_record import AttendanceRecord
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.lecturer import Lecturer
from app.models.class_section import ClassSection


# ============================================================
# GET ATTENDANCE SESSION
# ============================================================

def get_attendance_session(
    db: Session,
    session_id: int,
) -> AttendanceSession:

    result = db.execute(
        select(AttendanceSession).where(
            AttendanceSession.sessionID == session_id
        )
    )

    session = result.scalar_one_or_none()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance session not found",
        )

    return session


# ============================================================
# CREATE ATTENDANCE SESSION
# ============================================================

def create_attendance_session(
    db: Session,
    user_id: int,
    class_id: int,
    session_date,
    start_time,
    end_time,
    attendance_method: str,
    attendance_password: str | None,
) -> AttendanceSession:

    # 1. Find lecturer from logged-in user
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 2. Check lecturer is assigned to this class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == class_id,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 3. Validate time
    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time",
        )

    # 4. Validate attendance method
    if attendance_method not in ["PASSWORD", "SELF_SUBMIT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid attendance method",
        )

    # 5. Password is required for PASSWORD method
    if attendance_method == "PASSWORD" and not attendance_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance password is required",
        )

    # 6. Hash attendance password
    password_hash = None

    if attendance_password:
        password_hash = hash_password(attendance_password)

    # 7. Create attendance session
    attendance_session = AttendanceSession(
        classID=class_id,
        sessionDate=session_date,
        startTime=start_time,
        endTime=end_time,
        attendanceMethod=attendance_method,
        attendancePasswordHash=password_hash,
        status="SCHEDULED",
    )

    db.add(attendance_session)

    # Flush to get sessionID before creating attendance records
    db.flush()

    # 8. Get all active students enrolled in this class
    result = db.execute(
        select(Enrollment, Student).join(
            Student,
            Enrollment.studentID == Student.studentID,
        ).where(
            Enrollment.classID == class_id,
            Enrollment.status == "ACTIVE",
        )
    )

    enrolled_students = result.all()

    # 9. Create PENDING attendance record for every enrolled student
    for enrollment, student in enrolled_students:
        attendance_record = AttendanceRecord(
            sessionID=attendance_session.sessionID,
            studentID=student.studentID,
            status="PENDING",
            checkInTime=None,
            method=None,
            remark=None,
        )
        db.add(attendance_record)

    # 10. Save session and attendance records
    db.commit()
    db.refresh(attendance_session)

    return attendance_session


# ============================================================
# OPEN ATTENDANCE SESSION
# ============================================================

def open_attendance_session(
    db: Session,
    session_id: int,
    user_id: int,
) -> AttendanceSession:

    # 1. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=session_id,
    )

    # 2. Find lecturer from logged-in user
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 3. Check lecturer is assigned to this class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == session.classID,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 4. Session must be SCHEDULED
    if session.status != "SCHEDULED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only scheduled sessions can be opened",
        )

    # 5. Open session
    session.status = "OPEN"

    db.commit()

    db.refresh(session)

    return session


# ============================================================
# STUDENT SUBMIT ATTENDANCE
# ============================================================

def submit_attendance(
    db: Session,
    session_id: int,
    user_id: int,
    password: str | None,
) -> AttendanceRecord:

    # 1. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=session_id,
    )

    # 2. Session must be OPEN
    if session.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance session is not open",
        )

    # 3. Find student from logged-in user
    result = db.execute(
        select(Student).where(
            Student.userID == user_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    # 4. Check student enrollment
    result = db.execute(
        select(Enrollment).where(
            Enrollment.studentID == student.studentID,
            Enrollment.classID == session.classID,
            Enrollment.status == "ACTIVE",
        )
    )

    enrollment = result.scalar_one_or_none()

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student is not enrolled in this class",
        )

    # 5. Find existing attendance record
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.sessionID == session_id,
            AttendanceRecord.studentID == student.studentID,
        )
    )

    attendance_record = result.scalar_one_or_none()

    # 6. Student cannot submit attendance twice
    if attendance_record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )

    if attendance_record.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already submitted",
        )

    # 7. Handle attendance method
    if session.attendanceMethod == "PASSWORD":

        # Password is required
        if not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance password is required",
            )

        # Password hash must exist
        if not session.attendancePasswordHash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance password is not configured",
            )

        # Verify password
        if not verify_password(
            password,
            session.attendancePasswordHash,
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid attendance password",
            )

        attendance_record.method = "PASSWORD"

    elif session.attendanceMethod == "SELF_SUBMIT":

        # No password required
        attendance_record.method = "SELF_SUBMIT"

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid attendance method",
        )

    # 8. Change PENDING → PRESENT
    attendance_record.status = "PRESENT"
    attendance_record.checkInTime = datetime.now(timezone.utc)
    attendance_record.remark = None

    # 9. Save
    db.commit()
    db.refresh(attendance_record)

    return attendance_record


# ============================================================
# STUDENT ATTENDANCE HISTORY
# ============================================================

def get_student_attendance_history(
    db: Session,
    user_id: int,
):

    # 1. Find student
    result = db.execute(
        select(Student).where(
            Student.userID == user_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    # 2. Get attendance records
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
            AttendanceRecord.studentID
            == student.studentID
        )
        .order_by(
            AttendanceSession.sessionDate.desc(),
            AttendanceSession.startTime.desc(),
        )
    )

    return result.all()


# ============================================================
# STUDENT ATTENDANCE PERCENTAGE
# ============================================================

def get_student_attendance_percentage(
    db: Session,
    user_id: int,
):

    # 1. Find student
    result = db.execute(
        select(Student).where(
            Student.userID == user_id
        )
    )

    student = result.scalar_one_or_none()

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    # 2. Get all attendance records
    result = db.execute(
        select(AttendanceRecord)
        .where(
            AttendanceRecord.studentID
            == student.studentID
        )
    )

    records = result.scalars().all()

    # 3. Count attendance statuses
    total = len(records)

    present = sum(
        1
        for record in records
        if record.status == "PRESENT"
    )

    late = sum(
        1
        for record in records
        if record.status == "LATE"
    )

    absent = sum(
        1
        for record in records
        if record.status == "ABSENT"
    )

    # 4. Calculate percentage
    if total == 0:
        percentage = 0
    else:
        percentage = round(
            ((present + late) / total) * 100,
            2,
        )

    return {
        "totalSessions": total,
        "present": present,
        "late": late,
        "absent": absent,
        "attendancePercentage": percentage,
    }


# ============================================================
# CLOSE ATTENDANCE SESSION
# ============================================================

def close_attendance_session(
    db: Session,
    session_id: int,
    user_id: int,
) -> AttendanceSession:

    # 1. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=session_id,
    )

    # 2. Find lecturer from logged-in user
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 3. Check lecturer is assigned to this class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == session.classID,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 4. Session must be OPEN
    if session.status != "OPEN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only open sessions can be closed",
        )

    # 5. Get all active students enrolled in this class
    result = db.execute(
        select(
            Enrollment,
            Student,
        )
        .join(
            Student,
            Enrollment.studentID
            == Student.studentID,
        )
        .where(
            Enrollment.classID == session.classID,
            Enrollment.status == "ACTIVE",
        )
    )

    enrolled_students = result.all()

    # 6. Mark students who did not attend as ABSENT
    for enrollment, student in enrolled_students:

        result = db.execute(
            select(AttendanceRecord).where(
                AttendanceRecord.sessionID == session_id,
                AttendanceRecord.studentID == student.studentID,
            )
        )

        existing_record = result.scalar_one_or_none()

        # Student has a PENDING record -> mark as ABSENT
        if existing_record is not None:
            if existing_record.status == "PENDING":
                existing_record.status = "ABSENT"
                existing_record.checkInTime = None
                existing_record.method = None
                existing_record.remark = (
                    "Automatically marked absent "
                    "when session closed"
                )

            continue

        # Safety fallback:
        # create ABSENT record if no record exists
        absent_record = AttendanceRecord(
            sessionID=session_id,
            studentID=student.studentID,
            status="ABSENT",
            checkInTime=None,
            method=None,
            remark=(
                "Automatically marked absent "
                "when session closed"
            ),
        )

        db.add(absent_record)

    # 7. Change session status to CLOSED
    session.status = "CLOSED"

    db.commit()

    db.refresh(session)

    return session
# ============================================================
# GET ATTENDANCE RECORDS - LECTURER
# ============================================================

def get_session_attendance_records(
    db: Session,
    session_id: int,
    user_id: int,
):
    # 1. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=session_id,
    )

    # 2. Find lecturer from logged-in user
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 3. Check lecturer is assigned to this class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == session.classID,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 4. Get attendance records
    result = db.execute(
        select(
            AttendanceRecord,
            Student,
        )
        .join(
            Student,
            AttendanceRecord.studentID
            == Student.studentID,
        )
        .where(
            AttendanceRecord.sessionID == session_id
        )
        .order_by(
            Student.studentCode
        )
    )

    return result.all()

# ============================================================
# UPDATE ATTENDANCE RECORD - LECTURER
# ============================================================

def update_attendance_record(
    db: Session,
    attendance_id: int,
    user_id: int,
    new_status: str,
    remark: str | None,
) -> AttendanceRecord:

    # 1. Validate attendance status
    allowed_statuses = [
        "PRESENT",
        "LATE",
        "ABSENT",
    ]

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid attendance status",
        )

    # 2. Find attendance record
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.attendanceID == attendance_id
        )
    )

    attendance = result.scalar_one_or_none()

    if attendance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )

    # 3. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=attendance.sessionID,
    )

    # 4. Find lecturer
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 5. Check lecturer owns the class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == session.classID,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 6. Update attendance
    attendance.status = new_status
    attendance.remark = remark

    # 7. Update check-in time
    if new_status == "ABSENT":
        attendance.checkInTime = None

    elif attendance.checkInTime is None:
        attendance.checkInTime = datetime.now(timezone.utc)

    # 8. Update method
    if new_status in ["PRESENT", "LATE"]:
        attendance.method = "LECTURER_MANUAL"
    else:
        attendance.method = None

    # 9. Save changes
    db.commit()
    db.refresh(attendance)

    return attendance

# ============================================================
# GET ATTENDANCE REPORT - LECTURER
# ============================================================

def get_attendance_report(
    db: Session,
    session_id: int,
    user_id: int,
):
    # 1. Get attendance session
    session = get_attendance_session(
        db=db,
        session_id=session_id,
    )

    # 2. Find lecturer from logged-in user
    result = db.execute(
        select(Lecturer).where(
            Lecturer.userID == user_id
        )
    )

    lecturer = result.scalar_one_or_none()

    if lecturer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lecturer profile not found",
        )

    # 3. Check lecturer owns this class
    result = db.execute(
        select(ClassSection).where(
            ClassSection.classID == session.classID,
            ClassSection.lecturerID == lecturer.lecturerID,
        )
    )

    class_section = result.scalar_one_or_none()

    if class_section is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Lecturer is not assigned to this class",
        )

    # 4. Get all attendance records
    result = db.execute(
        select(AttendanceRecord).where(
            AttendanceRecord.sessionID == session_id
        )
    )

    records = result.scalars().all()

    # 5. Count attendance status
    total_students = len(records)

    present = sum(
        1
        for record in records
        if record.status == "PRESENT"
    )

    late = sum(
        1
        for record in records
        if record.status == "LATE"
    )

    absent = sum(
        1
        for record in records
        if record.status == "ABSENT"
    )

    # 6. Calculate attendance percentage
    if total_students == 0:
        attendance_percentage = 0.0
    else:
        attendance_percentage = round(
            ((present + late) / total_students) * 100,
            2,
        )

    # 7. Return report
    return {
        "sessionID": session_id,
        "totalStudents": total_students,
        "present": present,
        "late": late,
        "absent": absent,
        "attendancePercentage": attendance_percentage,
    }