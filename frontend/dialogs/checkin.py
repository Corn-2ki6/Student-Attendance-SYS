from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class CheckInDialog(QDialog):
    def __init__(self, attendance_api, parent=None):
        super().__init__(parent)

        self.attendance_api = attendance_api

        self.setWindowTitle("Submit Attendance")
        self.setMinimumWidth(480)

        layout = QVBoxLayout(self)

        # =========================
        # TITLE
        # =========================

        title = QLabel("Attendance Check-in")
        title.setObjectName("pageTitle")

        layout.addWidget(title)

        # =========================
        # DESCRIPTION
        # =========================

        description = QLabel(
            "The backend currently requires a session ID "
            "when submitting attendance.\n"
            "Enter the session ID provided by your lecturer "
            "and the password if the attendance method is PASSWORD."
        )

        description.setWordWrap(True)
        description.setObjectName("muted")

        layout.addWidget(description)

        # =========================
        # SESSION ID
        # =========================

        session_label = QLabel("Session ID")
        layout.addWidget(session_label)

        self.session_id = QLineEdit()

        self.session_id.setPlaceholderText(
            "Example: 1"
        )

        layout.addWidget(self.session_id)

        # =========================
        # PASSWORD
        # =========================

        password_label = QLabel("Password")
        layout.addWidget(password_label)

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Leave blank for SELF_SUBMIT"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        layout.addWidget(self.password)

        # =========================
        # SUBMIT BUTTON
        # =========================

        submit_button = QPushButton(
            "SUBMIT ATTENDANCE"
        )

        submit_button.setObjectName(
            "primaryButton"
        )

        submit_button.clicked.connect(
            self.submit
        )

        layout.addWidget(submit_button)

    # =========================
    # SUBMIT ATTENDANCE
    # =========================

    def submit(self):
        session_id_text = (
            self.session_id.text().strip()
        )

        password = (
            self.password.text()
        )

        if not session_id_text:
            QMessageBox.warning(
                self,
                "Submit Attendance",
                "Please enter a session ID.",
            )

            return

        try:
            session_id = int(
                session_id_text
            )

        except ValueError:
            QMessageBox.warning(
                self,
                "Submit Attendance",
                "Session ID must be a number.",
            )

            return

        try:
            self.attendance_api.submit(
                session_id,
                password or None,
            )

            QMessageBox.information(
                self,
                "Attendance",
                "Attendance submitted successfully.",
            )

            self.accept()

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Submit Attendance",
                str(exc),
            )
