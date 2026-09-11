from datetime import time

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.class_section import ClassSection
from app.models.schedule import Schedule


def create_test_schedule():
    db = SessionLocal()

    try:
        class_section = db.execute(
            select(ClassSection).where(
                ClassSection.classCode == "IR101-01"
            )
        ).scalar_one_or_none()

        if class_section is None:
            print("Class 'IR101-01' does not exist.")
            return

        existing_schedule = db.execute(
            select(Schedule).where(
                Schedule.classID == class_section.classID
            )
        ).scalar_one_or_none()

        if existing_schedule:
            print("Schedule already exists.")
            print(f"Schedule ID: {existing_schedule.scheduleID}")
            return

        schedule = Schedule(
            classID=class_section.classID,
            dayOfWeek="MONDAY",
            startTime=time(8, 0),
            endTime=time(10, 0),
            room="A101",
        )

        db.add(schedule)
        db.commit()
        db.refresh(schedule)

        print("Test schedule created successfully!")
        print(f"Schedule ID: {schedule.scheduleID}")
        print(f"Class ID: {schedule.classID}")
        print(f"Day: {schedule.dayOfWeek}")
        print(f"Time: {schedule.startTime} - {schedule.endTime}")
        print(f"Room: {schedule.room}")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_test_schedule()