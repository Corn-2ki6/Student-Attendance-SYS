from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from pages.base import BasePage
from api.client import ApiError


class SchedulePage(BasePage):
    def __init__(self, profile, navigate, logout, student_api):
        super().__init__("Weekly Schedule", profile, navigate, logout)
        self.api = student_api
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Day", "Time", "Course code", "Course", "Class", "Room"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.body.addWidget(self.table)
        self.refresh()

    def refresh(self):
        try:
            data = self.api.schedule()
            self.table.setRowCount(len(data))
            for r, item in enumerate(data):
                values = [item.get("dayOfWeek"), f"{item.get('startTime','')} - {item.get('endTime','')}", item.get("courseCode"), item.get("courseName"), item.get("classCode"), item.get("room")]
                for c, value in enumerate(values): self.table.setItem(r, c, QTableWidgetItem(str(value or "")))
        except ApiError as exc:
            QMessageBox.warning(self, "Schedule", str(exc))
