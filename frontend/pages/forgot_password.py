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


class ForgotPasswordPage(QWidget):

    def __init__(
        self,
        auth_api,
        show_login,
    ):
        super().__init__()

        self.auth_api = auth_api
        self.show_login = show_login
        self.reset_token = None

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(460)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(38, 38, 38, 38)
        layout.setSpacing(14)

        title = QLabel("Forgot Password")
        title.setObjectName("loginTitle")

        subtitle = QLabel(
            "Verify your username and email, then set a new password."
        )
        subtitle.setObjectName("muted")
        subtitle.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.request_button = QPushButton("REQUEST RESET TOKEN")
        self.request_button.setObjectName("primaryButton")
        self.request_button.setCursor(Qt.PointingHandCursor)
        self.request_button.clicked.connect(self.request_reset_token)

        layout.addWidget(self.username)
        layout.addWidget(self.email)
        layout.addWidget(self.request_button)

        self.token_label = QLabel("Reset token")
        self.token_label.setObjectName("muted")
        self.token_label.setVisible(False)

        self.reset_token_input = QLineEdit()
        self.reset_token_input.setPlaceholderText("Reset token")
        self.reset_token_input.setVisible(False)

        self.new_password = QLineEdit()
        self.new_password.setPlaceholderText("New password")
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setVisible(False)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Confirm new password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setVisible(False)
        self.confirm_password.returnPressed.connect(self.reset_password)

        self.reset_button = QPushButton("RESET PASSWORD")
        self.reset_button.setObjectName("primaryButton")
        self.reset_button.setCursor(Qt.PointingHandCursor)
        self.reset_button.clicked.connect(self.reset_password)
        self.reset_button.setVisible(False)

        layout.addWidget(self.token_label)
        layout.addWidget(self.reset_token_input)
        layout.addWidget(self.new_password)
        layout.addWidget(self.confirm_password)
        layout.addWidget(self.reset_button)

        back_button = QPushButton("BACK TO LOGIN")
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.clicked.connect(self.show_login)

        layout.addWidget(back_button)

        root.addWidget(card)

    def request_reset_token(self):
        username = self.username.text().strip()
        email = self.email.text().strip()

        if not username or not email:
            QMessageBox.warning(
                self,
                "Forgot Password",
                "Please enter your username and email.",
            )
            return

        try:
            result = self.auth_api.forgot_password(
                username,
                email,
            )

            self.reset_token = result.get("reset_token")
            if not self.reset_token:
                QMessageBox.warning(
                    self,
                    "Forgot Password",
                    "Backend did not return a reset token.",
                )
                return

            self.reset_token_input.setText(self.reset_token)

            self.token_label.setVisible(True)
            self.reset_token_input.setVisible(True)
            self.new_password.setVisible(True)
            self.confirm_password.setVisible(True)
            self.reset_button.setVisible(True)

            QMessageBox.information(
                self,
                "Forgot Password",
                "Account verified. Enter a new password to continue.",
            )

        except ApiError as exc:
            QMessageBox.warning(
                self,
                "Forgot Password",
                str(exc),
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Forgot Password",
                f"Unexpected error:\n{exc}",
            )

    def reset_password(self):
        username = self.username.text().strip()
        reset_token = self.reset_token_input.text().strip()
        new_password = self.new_password.text()
        confirm_password = self.confirm_password.text()

        if not reset_token:
            QMessageBox.warning(
                self,
                "Reset Password",
                "Please request a reset token first.",
            )
            return

        if len(new_password) < 6:
            QMessageBox.warning(
                self,
                "Reset Password",
                "New password must be at least 6 characters.",
            )
            return

        if new_password != confirm_password:
            QMessageBox.warning(
                self,
                "Reset Password",
                "Password confirmation does not match.",
            )
            return

        try:
            self.auth_api.reset_password(
                username,
                reset_token,
                new_password,
            )

            QMessageBox.information(
                self,
                "Reset Password",
                "Password reset successfully. You can now log in.",
            )

            self.clear_form()
            self.show_login()

        except ApiError as exc:
            QMessageBox.warning(
                self,
                "Reset Password",
                str(exc),
            )

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Reset Password",
                f"Unexpected error:\n{exc}",
            )

    def clear_form(self):
        self.username.clear()
        self.email.clear()
        self.reset_token_input.clear()
        self.new_password.clear()
        self.confirm_password.clear()
        self.reset_token = None

        self.token_label.setVisible(False)
        self.reset_token_input.setVisible(False)
        self.new_password.setVisible(False)
        self.confirm_password.setVisible(False)
        self.reset_button.setVisible(False)
