from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel


class Header(QWidget):
    def __init__(self, title, profile):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        title_label = QLabel(title)
        title_label.setObjectName("pageTitle")
        user = QLabel(profile.get("fullName", "Student"))
        user.setObjectName("headerUser")
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(user)
