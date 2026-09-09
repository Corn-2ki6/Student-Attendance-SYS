from fastapi import FastAPI

app = FastAPI(
    title="Student Attendance System API",
    description="Backend API for Student Attendance System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Student Attendance System API is running"
    }