from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


class LecturerSidebar(QWidget):
    navigate = Signal(str)
    logout_clicked = Signal()

    def __init__(self, profile):
        super().__init__()

        self.setObjectName("sidebar")
        self.setFixedWidth(235)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(7)

        # Logo
        logo = QLabel("LECTURER")
        logo.setObjectName("logo")

        sub = QLabel("Attendance System")
        sub.setObjectName("sidebarSub")

        layout.addWidget(logo)
        layout.addWidget(sub)
        layout.addSpacing(24)

        # Navigation
        menu_items = [
            ("Dashboard", "dashboard"),
            ("My Classes", "classes"),
            ("Attendance Sessions", "sessions"),
            ("My Profile", "profile"),
        ]

        for text, key in menu_items:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCursor(Qt.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, k=key:
                self.navigate.emit(k)
            )

            layout.addWidget(button)

        layout.addStretch()

        # Lecturer information
        full_name = profile.get(
            "fullName",
            "Lecturer"
        )

        lecturer_code = profile.get(
            "lecturerCode",
            ""
        )

        who = QLabel(
            f"{full_name}\n{lecturer_code}"
        )

        who.setObjectName("miniUser")

        layout.addWidget(who)

        # Logout
        logout = QPushButton("Log out")
        logout.setObjectName("logoutButton")
        logout.setCursor(Qt.PointingHandCursor)

        logout.clicked.connect(
            self.logout_clicked.emit
        )

        layout.addWidget(logout)