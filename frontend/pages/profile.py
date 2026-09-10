from PySide6.QtWidgets import QFrame, QFormLayout, QLabel, QPushButton
from pages.base import BasePage
from dialogs.change_password import ChangePasswordDialog


class ProfilePage(BasePage):
    def __init__(self, profile, navigate, logout, student_api):
        super().__init__("My Profile", profile, navigate, logout)
        self.api = student_api
        card = QFrame(); card.setObjectName("card")
        form = QFormLayout(card); form.setContentsMargins(24, 24, 24, 24); form.setSpacing(14)
        fields = [
            ("Student ID", profile.get("studentID")),
            ("Student code", profile.get("studentCode")),
            ("Full name", profile.get("fullName")),
            ("Date of birth", profile.get("dateOfBirth")),
            ("Gender", profile.get("gender")),
            ("Major", profile.get("major")),
        ]
        for key, value in fields:
            label = QLabel(str(value or "—")); label.setObjectName("profileValue"); form.addRow(key, label)
        btn = QPushButton("CHANGE PASSWORD"); btn.setObjectName("primaryButton")
        btn.clicked.connect(lambda: ChangePasswordDialog(self.api, self).exec())
        form.addRow("", btn)
        self.body.addWidget(card); self.body.addStretch()
