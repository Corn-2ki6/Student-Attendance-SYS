from datetime import date, time

from pydantic import BaseModel


# ============================================================
# STUDENT SUBMIT ATTENDANCE
# ============================================================

class AttendanceSubmitRequest(BaseModel):
    password: str | None = None


# ============================================================
# LECTURER CREATE ATTENDANCE SESSION
# ============================================================

class AttendanceSessionCreateRequest(BaseModel):
    classID: int
    sessionDate: date
    startTime: time
    endTime: time
    attendanceMethod: str
    attendancePassword: str | None = None


# ============================================================
# LECTURER UPDATE ATTENDANCE RECORD
# ============================================================

class AttendanceRecordUpdateRequest(BaseModel):
    status: str
    remark: str | None = None

# ============================================================
# ATTENDANCE REPORT
# ============================================================

class AttendanceReportResponse(BaseModel):
    sessionID: int
    totalStudents: int
    present: int
    late: int
    absent: int
    attendancePercentage: float