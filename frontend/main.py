import os
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QMessageBox,
)

from api.client import ApiClient, ApiError
from api.auth import AuthApi
from api.student import StudentApi
from api.attendance import AttendanceApi
from api.lecturer import LecturerApi

from pages.login import LoginPage
from pages.register import RegisterPage

# =========================
# STUDENT PAGES
# =========================

from pages.dashboard import DashboardPage
from pages.classes import ClassesPage
from pages.attendance import AttendancePage
from pages.schedule import SchedulePage
from pages.profile import ProfilePage

# =========================
# LECTURER PAGES
# =========================

from pages.lecturer_dashboard import LecturerDashboardPage
from pages.lecturer_classes import LecturerClassesPage
from pages.lecturer_sessions import LecturerSessionsPage
from pages.lecturer_profile import LecturerProfilePage


class AttendanceApplication(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Student Attendance System"
        )

        self.resize(1280, 760)
        self.setMinimumSize(1000, 650)

        # =================================
        # API
        # =================================

        self.client = ApiClient()

        self.auth = AuthApi(
            self.client
        )

        self.student_api = StudentApi(
            self.client
        )

        self.attendance_api = AttendanceApi(
            self.client
        )

        self.lecturer_api = LecturerApi(
            self.client
        )

        # =================================
        # STACKED WIDGET
        # =================================

        self.stack = QStackedWidget()

        self.setCentralWidget(
            self.stack
        )

        self.pages = {}

        # =================================
        # LOGIN
        # =================================

        self.login = LoginPage(
            self.auth,
            self.handle_login,
            self.show_register,
        )

        self.stack.addWidget(
            self.login
        )

        # =================================
        # REGISTER
        # =================================

        self.register_page = RegisterPage(
            self.auth,
            self.show_login,
        )

        self.stack.addWidget(
            self.register_page
        )

    # =====================================
    # SHOW REGISTER
    # =====================================

    def show_register(self):
        self.register_page.clear_form()

        self.stack.setCurrentWidget(
            self.register_page
        )

    # =====================================
    # SHOW LOGIN
    # =====================================

    def show_login(self):
        self.register_page.clear_form()

        self.stack.setCurrentWidget(
            self.login
        )

    # =====================================
    # LOGIN ROUTING
    # =====================================

    def handle_login(self, user):

        role = user.get("role")

        if role == "STUDENT":

            self.build_student_ui()

        elif role == "LECTURER":

            self.build_lecturer_ui()

        else:

            self.auth.logout()

            QMessageBox.warning(
                self,
                "Access Denied",
                "Invalid account role.",
            )

    # =====================================
    # STUDENT UI
    # =====================================

    def build_student_ui(self):

        try:

            profile = (
                self.student_api.profile()
            )

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Profile Error",
                str(exc),
            )

            return

        self.profile = profile

        self.clear_pages()

        self.pages = {

            "dashboard": DashboardPage(
                profile,
                self.navigate,
                self.logout,
                self.student_api,
                self.attendance_api,
            ),

            "classes": ClassesPage(
                profile,
                self.navigate,
                self.logout,
                self.student_api,
            ),

            "attendance": AttendancePage(
                profile,
                self.navigate,
                self.logout,
                self.attendance_api,
            ),

            "schedule": SchedulePage(
                profile,
                self.navigate,
                self.logout,
                self.student_api,
            ),

            "profile": ProfilePage(
                profile,
                self.navigate,
                self.logout,
                self.student_api,
            ),
        }

        self.add_pages()

        self.stack.setCurrentWidget(
            self.pages["dashboard"]
        )

    # =====================================
    # LECTURER UI
    # =====================================

    def build_lecturer_ui(self):

        try:

            profile = (
                self.lecturer_api.profile()
            )

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Lecturer Profile Error",
                str(exc),
            )

            self.auth.logout()

            return

        self.profile = profile

        self.clear_pages()

        # =================================
        # ALL LECTURER PAGES
        # =================================

        self.pages = {

            # Dashboard
            "dashboard": LecturerDashboardPage(
                profile,
                self.navigate,
                self.logout,
                self.lecturer_api,
            ),

            # My Classes
            "classes": LecturerClassesPage(
                profile,
                self.navigate,
                self.logout,
                self.lecturer_api,
            ),

            # Attendance Sessions
            "sessions": LecturerSessionsPage(
                profile,
                self.navigate,
                self.logout,
                self.lecturer_api,
            ),

            # My Profile
            "profile": LecturerProfilePage(
                profile,
                self.navigate,
                self.logout,
                self.lecturer_api,
            ),
        }

        self.add_pages()

        # =================================
        # LOAD DASHBOARD
        # =================================

        dashboard = self.pages[
            "dashboard"
        ]

        try:

            dashboard.refresh()

        except Exception as exc:

            dashboard.welcome_text.setText(
                "Unable to load lecturer information.\n"
                f"{exc}"
            )

        self.stack.setCurrentWidget(
            self.pages["dashboard"]
        )

    # =====================================
    # ADD PAGES
    # =====================================

    def add_pages(self):

        for page in self.pages.values():

            self.stack.addWidget(
                page
            )

    # =====================================
    # CLEAR PAGES
    # =====================================

    def clear_pages(self):

        for page in list(
            self.pages.values()
        ):

            self.stack.removeWidget(
                page
            )

            page.deleteLater()

        self.pages = {}

    # =====================================
    # NAVIGATION
    # =====================================

    def navigate(self, key):

        page = self.pages.get(
            key
        )

        if page is None:

            QMessageBox.warning(
                self,
                "Navigation",
                f"Page not found: {key}",
            )

            return

        # =================================
        # REFRESH PAGE DATA
        # =================================

        if hasattr(
            page,
            "refresh",
        ):

            try:

                page.refresh()

            except ApiError as exc:

                QMessageBox.warning(
                    self,
                    "API Error",
                    str(exc),
                )

                return

            except Exception as exc:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(exc),
                )

                return

        self.stack.setCurrentWidget(
            page
        )

    # =====================================
    # LOGOUT
    # =====================================

    def logout(self):

        self.auth.logout()

        self.clear_pages()

        self.login.username.clear()
        self.login.password.clear()

        self.stack.setCurrentWidget(
            self.login
        )


# =========================================
# APPLICATION ENTRY POINT
# =========================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    qss = os.path.join(
        os.path.dirname(__file__),
        "style.qss",
    )

    with open(
        qss,
        "r",
        encoding="utf-8",
    ) as f:

        app.setStyleSheet(
            f.read()
        )

    window = AttendanceApplication()

    window.show()

    sys.exit(
        app.exec()
    )