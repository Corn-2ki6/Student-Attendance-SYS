from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.students import router as students_router
from app.routers.attendance import router as attendance_router
from app.routers.lecturers import router as lecturers_router


app = FastAPI(
    title="Student Attendance System API",
    description="Backend API for Student Attendance System",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(students_router)
app.include_router(attendance_router)
app.include_router(lecturers_router)


@app.get("/")
def root():
    return {
        "message": "Student Attendance System API is running"
    }