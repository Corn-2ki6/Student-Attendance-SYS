import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from api.client import ApiClient, ApiError
from api.auth import AuthApi
from api.student import StudentApi
from api.attendance import AttendanceApi
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from pages.classes import ClassesPage
from pages.attendance import AttendancePage
from pages.schedule import SchedulePage
from pages.profile import ProfilePage


class StudentApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Attendance System")
        self.resize(1280, 760)
        self.setMinimumSize(1000, 650)
        self.client = ApiClient()
        self.auth = AuthApi(self.client)
        self.student_api = StudentApi(self.client)
        self.attendance_api = AttendanceApi(self.client)
        self.stack = QStackedWidget(); self.setCentralWidget(self.stack)
        self.login = LoginPage(self.auth, self.build_student_ui)
        self.stack.addWidget(self.login)
        self.pages = {}

    def build_student_ui(self):
        try:
            profile = self.student_api.profile()
        except ApiError as exc:
            QMessageBox.warning(self, "Profile", str(exc)); return
        self.profile = profile
        self.pages = {
            "dashboard": DashboardPage(profile, self.navigate, self.logout, self.student_api, self.attendance_api),
            "classes": ClassesPage(profile, self.navigate, self.logout, self.student_api),
            "attendance": AttendancePage(profile, self.navigate, self.logout, self.attendance_api),
            "schedule": SchedulePage(profile, self.navigate, self.logout, self.student_api),
            "profile": ProfilePage(profile, self.navigate, self.logout, self.student_api),
        }
        for page in self.pages.values(): self.stack.addWidget(page)
        self.stack.setCurrentWidget(self.pages["dashboard"])

    def navigate(self, key):
        page = self.pages.get(key)
        if page:
            if hasattr(page, "refresh"): page.refresh()
            self.stack.setCurrentWidget(page)

    def logout(self):
        self.auth.logout()
        for page in list(self.pages.values()):
            self.stack.removeWidget(page); page.deleteLater()
        self.pages = {}
        self.login.password.clear()
        self.stack.setCurrentWidget(self.login)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qss = os.path.join(os.path.dirname(__file__), "style.qss")
    with open(qss, "r", encoding="utf-8") as f: app.setStyleSheet(f.read())
    window = StudentApplication(); window.show()
    sys.exit(app.exec())
