from datetime import date

from app.core.database import SessionLocal
from app.core.security import hash_password

from app.models.user import User
from app.models.student import Student
from app.models.enrollment import Enrollment


db = SessionLocal()

try:
    # ========================================================
    # 1. Create User 02
    # ========================================================

    user = User(
        userName="student02",
        passwordHash=hash_password("123456"),
        fullName="Test Student 02",
        email="student02@example.com",
        status="ACTIVE",
        role="STUDENT",
    )

    db.add(user)
    db.flush()

    print("Created User:")
    print("userID:", user.userID)

    # ========================================================
    # 2. Create Student 02
    # ========================================================

    student = Student(
        userID=user.userID,
        studentCode="SV002",
        fullName="Test Student 02",
        dateOfBirth=None,
        gender=None,
        major="International Relations",
    )

    db.add(student)
    db.flush()

    print("Created Student:")
    print("studentID:", student.studentID)

    # ========================================================
    # 3. Enroll Student 02 into Class 1
    # ========================================================

    enrollment = Enrollment(
        studentID=student.studentID,
        classID=1,
        enrollmentDate=date.today(),
        status="ACTIVE",
    )

    db.add(enrollment)

    db.commit()

    print("Created Enrollment:")
    print("classID: 1")
    print("studentID:", student.studentID)

    print("\nStudent 02 created successfully!")
    print("Username: student02")
    print("Password: 123456")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()