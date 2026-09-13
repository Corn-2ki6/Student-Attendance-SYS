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


class LoginPage(QWidget):

    def __init__(
        self,
        auth_api,
        logged_in,
        show_register=None,
        show_forgot_password=None,
    ):
        super().__init__()

        self.auth_api = auth_api
        self.logged_in = logged_in
        self.show_register = show_register
        self.show_forgot_password = show_forgot_password

        # =================================
        # MAIN LAYOUT
        # =================================

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        # =================================
        # LOGIN CARD
        # =================================

        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(430)

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            38,
            38,
            38,
            38,
        )

        layout.setSpacing(14)

        # =================================
        # TITLE
        # =================================

        title = QLabel(
            "Attendance System"
        )

        title.setObjectName(
            "loginTitle"
        )

        subtitle = QLabel(
            "Sign in with your Student or Lecturer account"
        )

        subtitle.setObjectName(
            "muted"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        # =================================
        # USERNAME
        # =================================

        self.username = QLineEdit()

        self.username.setPlaceholderText(
            "Username"
        )

        # =================================
        # PASSWORD
        # =================================

        self.password = QLineEdit()

        self.password.setPlaceholderText(
            "Password"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        self.password.returnPressed.connect(
            self.login
        )

        # =================================
        # LOGIN BUTTON
        # =================================

        login_button = QPushButton(
            "LOGIN"
        )

        login_button.setObjectName(
            "primaryButton"
        )

        login_button.setCursor(
            Qt.PointingHandCursor
        )

        login_button.clicked.connect(
            self.login
        )

        layout.addWidget(
            self.username
        )

        layout.addWidget(
            self.password
        )

        layout.addWidget(
            login_button
        )

        # =================================
        # FORGOT PASSWORD
        # =================================

        if self.show_forgot_password is not None:

            forgot_button = QPushButton(
                "FORGOT PASSWORD?"
            )

            forgot_button.setObjectName(
                "linkButton"
            )

            forgot_button.setCursor(
                Qt.PointingHandCursor
            )

            forgot_button.clicked.connect(
                self.show_forgot_password
            )

            layout.addWidget(
                forgot_button
            )

        # =================================
        # REGISTER BUTTON
        # =================================

        if self.show_register is not None:

            register_button = QPushButton(
                "CREATE STUDENT ACCOUNT"
            )

            register_button.setCursor(
                Qt.PointingHandCursor
            )

            register_button.clicked.connect(
                self.show_register
            )

            layout.addWidget(
                register_button
            )

        root.addWidget(card)

    # =====================================
    # LOGIN
    # =====================================

    def login(self):

        username = self.username.text().strip()
        password = self.password.text()

        # =================================
        # VALIDATION
        # =================================

        if not username or not password:

            QMessageBox.warning(
                self,
                "Login",
                "Please enter your username and password.",
            )

            return

        # =================================
        # API LOGIN
        # =================================

        try:

            user = self.auth_api.login(
                username,
                password,
            )

            role = user.get(
                "role"
            )

            # =================================
            # VALID ROLE
            # =================================

            if role not in (
                "STUDENT",
                "LECTURER",
            ):

                self.auth_api.logout()

                QMessageBox.warning(
                    self,
                    "Access Denied",
                    "This account is not allowed to use this application.",
                )

                return

            # =================================
            # LOGIN SUCCESS
            # =================================

            self.logged_in(user)

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Login Failed",
                str(exc),
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Login Error",
                f"Unexpected error:\n{exc}",
            )