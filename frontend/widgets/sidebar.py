from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class Sidebar(QWidget):
    navigate = Signal(str)
    logout_clicked = Signal()

    def __init__(self, profile):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(235)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(7)

        logo = QLabel("STUDENT")
        logo.setObjectName("logo")
        sub = QLabel("Attendance System")
        sub.setObjectName("sidebarSub")
        layout.addWidget(logo)
        layout.addWidget(sub)
        layout.addSpacing(24)

        for text, key in [
            ("Dashboard", "dashboard"),
            ("My Classes", "classes"),
            ("Attendance", "attendance"),
            ("Schedule", "schedule"),
            ("My Profile", "profile"),
        ]:
            btn = QPushButton(text)
            btn.setObjectName("navButton")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked=False, k=key: self.navigate.emit(k))
            layout.addWidget(btn)

        layout.addStretch()
        who = QLabel(f"{profile.get('fullName', 'Student')}\n{profile.get('studentCode', '')}")
        who.setObjectName("miniUser")
        layout.addWidget(who)
        logout = QPushButton("Log out")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(self.logout_clicked.emit)
        layout.addWidget(logout)
