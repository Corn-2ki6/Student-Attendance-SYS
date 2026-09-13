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
        super().__init__(
            "Attendance History",
            profile,
            navigate,
            logout,
        )

        self.api = attendance_api

        # =========================
        # TOP BUTTONS
        # =========================

        top = QHBoxLayout()
        top.addStretch()

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)

        check_button = QPushButton("CHECK IN")
        check_button.setObjectName("primaryButton")
        check_button.clicked.connect(self.check_in)

        top.addWidget(refresh_button)
        top.addWidget(check_button)

        self.body.addLayout(top)

        # =========================
        # ATTENDANCE TABLE
        # =========================

        self.table = QTableWidget(0, 8)

        self.table.setHorizontalHeaderLabels(
            [
                "Session ID",
                "Date",
                "Time",
                "Class ID",
                "Status",
                "Check-in",
                "Method",
                "Remark",
            ]
        )

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)

        self.body.addWidget(self.table)

        self.refresh()

    # =========================
    # LOAD ATTENDANCE HISTORY
    # =========================

    def refresh(self):
        try:
            rows = self.api.history()

            if rows is None:
                rows = []

            self.table.setRowCount(len(rows))

            for row_index, item in enumerate(rows):
                check_time = item.get("checkInTime") or ""

                values = [
                    item.get("sessionID"),
                    item.get("sessionDate"),
                    (
                        f"{item.get('startTime', '')} - "
                        f"{item.get('endTime', '')}"
                    ),
                    item.get("classID"),
                    item.get("status"),
                    check_time,
                    item.get("method"),
                    item.get("remark") or "",
                ]

                for column_index, value in enumerate(values):
                    table_item = QTableWidgetItem(
                        str(value or "")
                    )

                    self.table.setItem(
                        row_index,
                        column_index,
                        table_item,
                    )

        except ApiError as exc:
            QMessageBox.warning(
                self,
                "Attendance",
                str(exc),
            )

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Attendance",
                f"Unable to load attendance history.\n{exc}",
            )

    # =========================
    # CHECK IN
    # =========================

    def check_in(self):
        dialog = CheckInDialog(self.api, self)
        )

        if dialog.exec():
            self.refresh()
