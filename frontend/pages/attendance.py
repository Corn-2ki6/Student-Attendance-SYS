from PySide6.QtWidgets import (
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox,
)
from pages.base import BasePage
from dialogs.checkin import CheckInDialog
from api.client import ApiError


class AttendancePage(BasePage):
    def __init__(self, profile, navigate, logout, attendance_api):
        super().__init__("Attendance History", profile, navigate, logout)
        self.api = attendance_api

        top = QHBoxLayout()
        top.addStretch()

        check = QPushButton("CHECK IN")
        check.setObjectName("primaryButton")
        check.clicked.connect(self.check_in)

        refresh = QPushButton("Refresh")
        refresh.clicked.connect(self.refresh)

        top.addWidget(refresh)
        top.addWidget(check)
        self.body.addLayout(top)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Session ID",
            "Date",
            "Time",
            "Class ID",
            "Status",
            "Check-in",
            "Method",
            "Remark",
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.body.addWidget(self.table)

        self.refresh()

    def refresh(self):
        try:
            rows = self.api.history()
            self.table.setRowCount(len(rows))

            for r, item in enumerate(rows):
                check_time = item.get("checkInTime") or ""

                values = [
                    item.get("sessionID"),
                    item.get("sessionDate"),
                    f"{item.get('startTime', '')} - {item.get('endTime', '')}",
                    item.get("classID"),
                    item.get("status"),
                    check_time,
                    item.get("method"),
                    item.get("remark") or "",
                ]

                for c, value in enumerate(values):
                    self.table.setItem(
                        r, c, QTableWidgetItem(str(value or ""))
                    )

        except ApiError as exc:
            QMessageBox.warning(self, "Attendance", str(exc))

    def submit_attendance(self, session_id, password=None):
        """Hàm xử lý gọi API điểm danh được CheckInDialog gọi tới."""
        try:
            # Gọi API submit điểm danh về Backend
            payload = {"sessionID": session_id}
            if password:
                payload["password"] = password

            result = self.api.submit(payload)
            QMessageBox.information(self, "Success", "Attendance submitted successfully!")
            self.refresh()
            return True
        except ApiError as exc:
            QMessageBox.warning(self, "Check-in Failed", str(exc))
            return False

    def check_in(self):
        dialog = CheckInDialog(attendance_api=self.api, parent=self)

        # Hộp thoại mở lên, khi điểm danh thành công sẽ reload lại bảng
        if dialog.exec():
            self.refresh()
