from PySide6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
)
from pages.base import BasePage
from widgets.stat_card import StatCard
from dialogs.checkin import CheckInDialog
from api.client import ApiError


class DashboardPage(BasePage):
    def __init__(self, profile, navigate, logout, student_api, attendance_api):
        super().__init__("Dashboard", profile, navigate, logout)
        self.student_api = student_api
        self.attendance_api = attendance_api

        cards = QHBoxLayout()
        self.rate = StatCard("Attendance rate", "--", "Present + Late")
        self.present = StatCard("Present", "--", "Attendance records")
        self.absent = StatCard("Absent", "--", "Attendance records")
        self.classes = StatCard("Classes", "--", "Active enrollments")

        for c in [self.rate, self.present, self.absent, self.classes]:
            cards.addWidget(c)
        self.body.addLayout(cards)

        card = QFrame()
        card.setObjectName("card")

        lay = QVBoxLayout(card)
        lay.setContentsMargins(22, 20, 22, 20)

        title = QLabel("Quick attendance")
        title.setObjectName("sectionTitle")

        txt = QLabel(
            "Submit attendance for an OPEN session using the session ID "
            "supplied by the lecturer."
        )
        txt.setObjectName("muted")
        txt.setWordWrap(True)

        btn = QPushButton("CHECK IN")
        btn.setObjectName("primaryButton")
        btn.clicked.connect(self.check_in)

        lay.addWidget(title)
        lay.addWidget(txt)
        lay.addSpacing(6)
        lay.addWidget(btn)

        self.body.addWidget(card)
        self.body.addStretch()
        self.refresh()

    def refresh(self):
        try:
            p = self.attendance_api.percentage()
            classes = self.student_api.classes()

            self.rate.set_value(f"{p.get('attendancePercentage', 0)}%")
            self.present.set_value(p.get("present", 0))
            self.absent.set_value(p.get("absent", 0))
            self.classes.set_value(len(classes))
        except ApiError as exc:
            QMessageBox.warning(self, "Dashboard", str(exc))

    def check_in(self):
        dialog = CheckInDialog(
            attendance_api=self.attendance_api,
            parent=self,
        )

        # Hộp thoại đã gửi điểm danh; chỉ cập nhật lại thống kê.
        if dialog.exec():
            self.refresh()
