from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from api.client import ApiError
from pages.base import BasePage
from widgets.lecturer_sidebar import LecturerSidebar


class LecturerProfilePage(BasePage):

    def __init__(
        self,
        profile,
        navigate,
        logout,
        lecturer_api,
    ):
        super().__init__(
            "My Profile",
            profile,
            navigate,
            logout,
            sidebar_class=LecturerSidebar,
        )

        self.profile = profile
        self.lecturer_api = lecturer_api

        self.build_ui()
        self.refresh()

    def build_ui(self):

        title = QLabel(
            "My Profile"
        )
        title.setObjectName(
            "pageTitle"
        )

        self.body.addWidget(
            title
        )

        # =================================
        # LECTURER INFORMATION
        # =================================

        profile_card = QFrame()
        profile_card.setObjectName(
            "card"
        )

        profile_layout = QVBoxLayout(
            profile_card
        )

        profile_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        section = QLabel(
            "Lecturer Information"
        )

        section.setObjectName(
            "sectionTitle"
        )

        profile_layout.addWidget(
            section
        )

        form = QFormLayout()

        form.setSpacing(
            12
        )

        self.lecturer_code = QLabel(
            "-"
        )

        self.full_name = QLabel(
            "-"
        )

        self.department = QLabel(
            "-"
        )

        form.addRow(
            "Lecturer Code:",
            self.lecturer_code,
        )

        form.addRow(
            "Full Name:",
            self.full_name,
        )

        form.addRow(
            "Department:",
            self.department,
        )

        profile_layout.addLayout(
            form
        )

        self.body.addWidget(
            profile_card
        )

        # =================================
        # CHANGE PASSWORD
        # =================================

        password_card = QFrame()

        password_card.setObjectName(
            "card"
        )

        password_layout = QVBoxLayout(
            password_card
        )

        password_layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        password_title = QLabel(
            "Change Password"
        )

        password_title.setObjectName(
            "sectionTitle"
        )

        password_layout.addWidget(
            password_title
        )

        self.current_password = QLineEdit()

        self.current_password.setPlaceholderText(
            "Current password"
        )

        self.current_password.setEchoMode(
            QLineEdit.Password
        )

        self.new_password = QLineEdit()

        self.new_password.setPlaceholderText(
            "New password"
        )

        self.new_password.setEchoMode(
            QLineEdit.Password
        )

        self.confirm_password = QLineEdit()

        self.confirm_password.setPlaceholderText(
            "Confirm new password"
        )

        self.confirm_password.setEchoMode(
            QLineEdit.Password
        )

        password_layout.addWidget(
            self.current_password
        )

        password_layout.addWidget(
            self.new_password
        )

        password_layout.addWidget(
            self.confirm_password
        )

        change_button = QPushButton(
            "Change Password"
        )

        change_button.setObjectName(
            "primaryButton"
        )

        change_button.clicked.connect(
            self.change_password
        )

        password_layout.addWidget(
            change_button
        )

        self.body.addWidget(
            password_card
        )

        self.body.addStretch()

    # =====================================
    # REFRESH PROFILE
    # =====================================

    def refresh(self):

        try:

            profile = (
                self.lecturer_api.profile()
            )

            self.profile = profile

            self.lecturer_code.setText(
                str(
                    profile.get(
                        "lecturerCode",
                        "-",
                    )
                )
            )

            self.full_name.setText(
                str(
                    profile.get(
                        "fullName",
                        "-",
                    )
                )
            )

            self.department.setText(
                str(
                    profile.get(
                        "department",
                        "-",
                    )
                )
            )

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Profile",
                str(exc),
            )

    # =====================================
    # CHANGE PASSWORD
    # =====================================

    def change_password(self):

        current = (
            self.current_password.text()
        )

        new = (
            self.new_password.text()
        )

        confirm = (
            self.confirm_password.text()
        )

        if not current or not new or not confirm:

            QMessageBox.warning(
                self,
                "Change Password",
                "Please fill in all fields.",
            )

            return

        if new != confirm:

            QMessageBox.warning(
                self,
                "Change Password",
                "New passwords do not match.",
            )

            return

        if len(new) < 6:

            QMessageBox.warning(
                self,
                "Change Password",
                "New password must be at least 6 characters long.",
            )

            return

        try:

            self.lecturer_api.change_password(
                current,
                new,
            )

            QMessageBox.information(
                self,
                "Change Password",
                "Password changed successfully.",
            )

            self.current_password.clear()
            self.new_password.clear()
            self.confirm_password.clear()

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Change Password",
                str(exc),
            )