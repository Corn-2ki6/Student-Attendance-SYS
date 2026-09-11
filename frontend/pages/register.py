from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)

from api.client import ApiError


class RegisterPage(QWidget):
    def __init__(
        self,
        auth_api,
        show_login,
    ):
        super().__init__()

        self.auth_api = auth_api
        self.show_login = show_login

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(470)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            38,
            38,
            38,
            38,
        )

        layout.setSpacing(12)

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel(
            "Create Student Account"
        )
        title.setObjectName("loginTitle")

        subtitle = QLabel(
            "Register a new student account"
        )
        subtitle.setObjectName("muted")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)

        # =====================================================
        # FULL NAME
        # =====================================================

        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText(
            "Full Name"
        )

        # =====================================================
        # EMAIL
        # =====================================================

        self.email = QLineEdit()
        self.email.setPlaceholderText(
            "Email"
        )

        # =====================================================
        # USERNAME
        # =====================================================

        self.username = QLineEdit()
        self.username.setPlaceholderText(
            "Username"
        )

        # =====================================================
        # PASSWORD
        # =====================================================

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Password"
        )
        self.password.setEchoMode(
            QLineEdit.Password
        )

        # =====================================================
        # CONFIRM PASSWORD
        # =====================================================

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText(
            "Confirm Password"
        )
        self.confirm_password.setEchoMode(
            QLineEdit.Password
        )

        self.confirm_password.returnPressed.connect(
            self.register
        )

        # =====================================================
        # REGISTER BUTTON
        # =====================================================

        register_button = QPushButton(
            "CREATE ACCOUNT"
        )

        register_button.setObjectName(
            "primaryButton"
        )

        register_button.setCursor(
            Qt.PointingHandCursor
        )

        register_button.clicked.connect(
            self.register
        )

        # =====================================================
        # BACK TO LOGIN
        # =====================================================

        login_button = QPushButton(
            "BACK TO LOGIN"
        )

        login_button.setCursor(
            Qt.PointingHandCursor
        )

        login_button.clicked.connect(
            self.show_login
        )

        # =====================================================
        # ADD WIDGETS
        # =====================================================

        layout.addWidget(
            self.full_name
        )

        layout.addWidget(
            self.email
        )

        layout.addWidget(
            self.username
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            self.confirm_password
        )

        layout.addSpacing(6)

        layout.addWidget(
            register_button
        )

        layout.addWidget(
            login_button
        )

        root.addWidget(card)

    # =========================================================
    # REGISTER
    # =========================================================

    def register(self):
        full_name = self.full_name.text().strip()
        email = self.email.text().strip()
        username = self.username.text().strip()
        password = self.password.text()
        confirm_password = (
            self.confirm_password.text()
        )

        # -----------------------------------------------------
        # VALIDATION
        # -----------------------------------------------------

        if not full_name:
            QMessageBox.warning(
                self,
                "Registration",
                "Please enter your full name.",
            )
            self.full_name.setFocus()
            return

        if not email:
            QMessageBox.warning(
                self,
                "Registration",
                "Please enter your email.",
            )
            self.email.setFocus()
            return

        if "@" not in email:
            QMessageBox.warning(
                self,
                "Registration",
                "Please enter a valid email address.",
            )
            self.email.setFocus()
            return

        if not username:
            QMessageBox.warning(
                self,
                "Registration",
                "Please enter a username.",
            )
            self.username.setFocus()
            return

        if not password:
            QMessageBox.warning(
                self,
                "Registration",
                "Please enter a password.",
            )
            self.password.setFocus()
            return

        if len(password) < 6:
            QMessageBox.warning(
                self,
                "Registration",
                "Password must be at least 6 characters.",
            )
            self.password.setFocus()
            return

        if password != confirm_password:
            QMessageBox.warning(
                self,
                "Registration",
                "Passwords do not match.",
            )
            self.confirm_password.clear()
            self.confirm_password.setFocus()
            return

        # -----------------------------------------------------
        # API
        # -----------------------------------------------------

        try:
            result = self.auth_api.register_student(
                full_name=full_name,
                email=email,
                username=username,
                password=password,
            )

            user = {}

            if isinstance(result, dict):
                user = result.get(
                    "user",
                    {},
                )

            student_code = user.get(
                "studentCode",
                "",
            )

            message = (
                "Registration completed successfully."
            )

            if student_code:
                message += (
                    f"\n\nYour Student Code: "
                    f"{student_code}"
                )

            QMessageBox.information(
                self,
                "Registration Successful",
                message,
            )

            self.clear_form()

            self.show_login()

        except ApiError as exc:
            QMessageBox.warning(
                self,
                "Registration Failed",
                str(exc),
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Registration Error",
                f"Unexpected error:\n{exc}",
            )

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):
        self.full_name.clear()
        self.email.clear()
        self.username.clear()
        self.password.clear()
        self.confirm_password.clear()