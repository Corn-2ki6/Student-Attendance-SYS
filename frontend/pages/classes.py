from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from pages.base import BasePage
from api.client import ApiError


class ClassesPage(BasePage):
    def __init__(self, profile, navigate, logout, student_api):
        super().__init__("My Classes", profile, navigate, logout)
        self.api = student_api
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Class", "Course code", "Course", "Credits", "Semester", "Academic year"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.body.addWidget(self.table)
        self.refresh()

    def refresh(self):
        try:
            data = self.api.classes()
            self.table.setRowCount(len(data))
            for r, item in enumerate(data):
                values = [item.get("classCode"), item.get("courseCode"), item.get("courseName"), item.get("credits"), item.get("semester"), item.get("academicYear")]
                for c, value in enumerate(values): self.table.setItem(r, c, QTableWidgetItem(str(value or "")))
        except ApiError as exc:
            QMessageBox.warning(self, "Classes", str(exc))
