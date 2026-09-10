from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox
from api.client import ApiError


class LoginPage(QWidget):
    def __init__(self, auth_api, logged_in):
        super().__init__()
        self.auth_api = auth_api
        self.logged_in = logged_in
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)
        card = QFrame()
        card.setObjectName("loginCard")
        card.setFixedWidth(430)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(38, 38, 38, 38)
        layout.setSpacing(14)
        title = QLabel("Student Attendance")
        title.setObjectName("loginTitle")
        sub = QLabel("Sign in with your student account")
        sub.setObjectName("muted")
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.login)
        btn = QPushButton("LOGIN")
        btn.setObjectName("primaryButton")
        btn.clicked.connect(self.login)
        hint = QLabel("Test backend script creates: student01 / 123456")
        hint.setObjectName("muted")
        layout.addWidget(title); layout.addWidget(sub); layout.addSpacing(8)
        layout.addWidget(self.username); layout.addWidget(self.password); layout.addWidget(btn); layout.addWidget(hint)
        root.addWidget(card)

    def login(self):
        if not self.username.text().strip() or not self.password.text():
            QMessageBox.warning(self, "Login", "Enter username and password.")
            return
        try:
            user = self.auth_api.login(self.username.text().strip(), self.password.text())
            if user.get("role") != "STUDENT":
                self.auth_api.logout()
                QMessageBox.warning(self, "Role", "This frontend is for STUDENT accounts only.")
                return
            self.logged_in()
        except ApiError as exc:
            QMessageBox.warning(self, "Login failed", str(exc))
