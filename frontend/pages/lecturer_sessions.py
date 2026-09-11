from PySide6.QtCore import Qt, QDate, QTime
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDateEdit,
    QTimeEdit,
    QLineEdit,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
)

from api.client import ApiError
from pages.base import BasePage
from widgets.lecturer_sidebar import LecturerSidebar


class CreateSessionDialog(QDialog):

    def __init__(self, classes, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Create Attendance Session"
        )

        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        form.setSpacing(12)

        self.class_combo = QComboBox()

        for item in classes:

            text = (
                f"{item.get('classCode', '')} - "
                f"{item.get('courseCode', '')} - "
                f"{item.get('courseName', '')}"
            )

            self.class_combo.addItem(
                text,
                item.get("classID"),
            )

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(
            QDate.currentDate()
        )

        self.start_time = QTimeEdit()
        self.start_time.setTime(
            QTime(7, 0)
        )

        self.end_time = QTimeEdit()
        self.end_time.setTime(
            QTime(9, 0)
        )

        self.method_combo = QComboBox()
        self.method_combo.addItems(
            [
                "PASSWORD",
                "QR",
                "MANUAL",
            ]
        )

        self.password = QLineEdit()
        self.password.setPlaceholderText(
            "Attendance password (optional)"
        )

        self.password.setEchoMode(
            QLineEdit.Password
        )

        form.addRow(
            "Class:",
            self.class_combo,
        )

        form.addRow(
            "Date:",
            self.date_edit,
        )

        form.addRow(
            "Start Time:",
            self.start_time,
        )

        form.addRow(
            "End Time:",
            self.end_time,
        )

        form.addRow(
            "Attendance Method:",
            self.method_combo,
        )

        form.addRow(
            "Password:",
            self.password,
        )

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
            | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            self.accept
        )

        buttons.rejected.connect(
            self.reject
        )

        layout.addWidget(buttons)

    def data(self):

        return {
            "class_id": self.class_combo.currentData(),
            "session_date": self.date_edit.date().toString(
                "yyyy-MM-dd"
            ),
            "start_time": self.start_time.time().toString(
                "HH:mm:ss"
            ),
            "end_time": self.end_time.time().toString(
                "HH:mm:ss"
            ),
            "attendance_method": self.method_combo.currentText(),
            "attendance_password": self.password.text()
            or None,
        }


class LecturerSessionsPage(BasePage):

    def __init__(
        self,
        profile,
        navigate,
        logout,
        lecturer_api,
    ):

        super().__init__(
            "Attendance Sessions",
            profile,
            navigate,
            logout,
            sidebar_class=LecturerSidebar,
        )

        self.profile = profile
        self.lecturer_api = lecturer_api
        self.classes = []
        self.sessions = []

        self.build_ui()
        self.refresh()

    def build_ui(self):

        title = QLabel(
            "Attendance Sessions"
        )
        title.setObjectName(
            "pageTitle"
        )

        self.body.addWidget(title)

        description = QLabel(
            "Manage attendance sessions for your assigned classes."
        )
        description.setObjectName(
            "muted"
        )

        self.body.addWidget(
            description
        )

        # =============================
        # FILTER
        # =============================

        filter_card = QFrame()
        filter_card.setObjectName("card")

        filter_layout = QHBoxLayout(
            filter_card
        )

        filter_layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        filter_layout.setSpacing(10)

        class_label = QLabel("Class:")
        class_label.setObjectName("muted")

        filter_layout.addWidget(
            class_label
        )

        self.class_filter = QComboBox()
        self.class_filter.setMinimumWidth(
            300
        )

        self.class_filter.currentIndexChanged.connect(
            self.refresh_sessions
        )

        filter_layout.addWidget(
            self.class_filter
        )

        date_label = QLabel("Date:")
        date_label.setObjectName("muted")

        filter_layout.addWidget(
            date_label
        )

        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(
            True
        )

        self.date_filter.setDate(
            QDate.currentDate()
        )

        self.date_filter.dateChanged.connect(
            self.refresh_sessions
        )

        filter_layout.addWidget(
            self.date_filter
        )

        status_label = QLabel("Status:")
        status_label.setObjectName("muted")

        filter_layout.addWidget(
            status_label
        )

        self.status_filter = QComboBox()

        self.status_filter.addItems(
            [
                "ALL",
                "OPEN",
                "CLOSED",
            ]
        )

        self.status_filter.currentIndexChanged.connect(
            self.refresh_sessions
        )

        filter_layout.addWidget(
            self.status_filter
        )

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setObjectName(
            "secondaryButton"
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        filter_layout.addWidget(
            refresh_button
        )

        create_button = QPushButton(
            "Create Session"
        )

        create_button.setObjectName(
            "primaryButton"
        )

        create_button.clicked.connect(
            self.create_session
        )

        filter_layout.addWidget(
            create_button
        )

        self.body.addWidget(
            filter_card
        )

        # =============================
        # SESSION TABLE
        # =============================

        self.table = QTableWidget()

        self.table.setColumnCount(9)

        self.table.setHorizontalHeaderLabels(
            [
                "Class",
                "Course",
                "Date",
                "Start Time",
                "End Time",
                "Method",
                "Status",
                "Open",
                "Details",
            ]
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.verticalHeader().setVisible(
            False
        )

        header = self.table.horizontalHeader()

        for column in range(9):

            header.setSectionResizeMode(
                column,
                QHeaderView.ResizeToContents,
            )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        self.body.addWidget(
            self.table
        )

    # =============================
    # LOAD CLASSES
    # =============================

    def refresh(self):

        try:

            self.classes = (
                self.lecturer_api.classes()
            )

            self.class_filter.blockSignals(
                True
            )

            self.class_filter.clear()

            self.class_filter.addItem(
                "All Classes",
                None,
            )

            for item in self.classes:

                text = (
                    f"{item.get('classCode', '')} - "
                    f"{item.get('courseCode', '')}"
                )

                self.class_filter.addItem(
                    text,
                    item.get("classID"),
                )

            self.class_filter.blockSignals(
                False
            )

            self.refresh_sessions()

        except ApiError as exc:

            self.class_filter.blockSignals(
                False
            )

            QMessageBox.warning(
                self,
                "Attendance Sessions",
                str(exc),
            )

    # =============================
    # LOAD SESSIONS
    # =============================

    def refresh_sessions(self):

        class_id = (
            self.class_filter.currentData()
        )

        session_date = (
            self.date_filter.date().toString(
                "yyyy-MM-dd"
            )
        )

        status = (
            self.status_filter.currentText()
        )

        if status == "ALL":
            status = None

        try:

            self.sessions = (
                self.lecturer_api.sessions(
                    class_id=class_id,
                    session_date=session_date,
                    status=status,
                )
            )

            self.table.setRowCount(
                len(self.sessions)
            )

            for row, session in enumerate(
                self.sessions
            ):

                values = [
                    session.get(
                        "classCode",
                        "",
                    ),
                    (
                        f"{session.get('courseCode', '')} - "
                        f"{session.get('courseName', '')}"
                    ),
                    session.get(
                        "sessionDate",
                        "",
                    ),
                    session.get(
                        "startTime",
                        "",
                    ),
                    session.get(
                        "endTime",
                        "",
                    ),
                    session.get(
                        "attendanceMethod",
                        "",
                    ),
                    session.get(
                        "status",
                        "",
                    ),
                ]

                for column, value in enumerate(
                    values
                ):

                    item = QTableWidgetItem(
                        str(value)
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                    self.table.setItem(
                        row,
                        column,
                        item,
                    )

                session_id = session.get(
                    "sessionID"
                )

                status_value = session.get(
                    "status",
                    ""
                )

                open_button = QPushButton(
                    "Open"
                )

                open_button.setObjectName(
                    "secondaryButton"
                )

                open_button.clicked.connect(
                    lambda checked=False,
                    sid=session_id:
                    self.open_session(sid)
                )

                if status_value == "OPEN":
                    open_button.setEnabled(
                        False
                    )

                if status_value == "CLOSED":
                    open_button.setEnabled(
                        False
                    )

                self.table.setCellWidget(
                    row,
                    7,
                    open_button,
                )

                details_button = QPushButton(
                    "View"
                )

                details_button.clicked.connect(
                    lambda checked=False,
                    sid=session_id:
                    self.view_session(sid)
                )

                self.table.setCellWidget(
                    row,
                    8,
                    details_button,
                )

        except ApiError as exc:

            self.table.setRowCount(0)

            QMessageBox.warning(
                self,
                "Sessions",
                str(exc),
            )

    # =============================
    # CREATE SESSION
    # =============================

    def create_session(self):

        if not self.classes:

            QMessageBox.warning(
                self,
                "Create Session",
                "You don't have any classes assigned yet.",
            )

            return

        dialog = CreateSessionDialog(
            self.classes,
            self,
        )

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.data()

        if data["class_id"] is None:

            QMessageBox.warning(
                self,
                "Create Session",
                "Please select a class.",
            )

            return

        if data["start_time"] >= data["end_time"]:

            QMessageBox.warning(
                self,
                "Create Session",
                "End time must be after start time.",
            )

            return

        try:

            self.lecturer_api.create_session(
                data["class_id"],
                data["session_date"],
                data["start_time"],
                data["end_time"],
                data["attendance_method"],
                data["attendance_password"],
            )

            QMessageBox.information(
                self,
                "Create Session",
                "Attendance session created successfully.",
            )

            self.refresh()

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Create Session",
                str(exc),
            )

    # =============================
    # OPEN SESSION
    # =============================

    def open_session(self, session_id):

        try:

            self.lecturer_api.open_session(
                session_id
            )

            QMessageBox.information(
                self,
                "Session",
                "Session has been opened successfully.",
            )

            self.refresh()

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Open Session",
                str(exc),
            )

    # =============================
    # VIEW SESSION
    # =============================

    def view_session(self, session_id):

        try:

            records = (
                self.lecturer_api.records(
                    session_id
                )
            )

            report = (
                self.lecturer_api.report(
                    session_id
                )
            )

            dialog = QDialog(self)

            dialog.setWindowTitle(
                f"Attendance Session #{session_id}"
            )

            dialog.resize(
                850,
                550,
            )

            layout = QVBoxLayout(
                dialog
            )

            summary = QLabel(
                f"Total Students: {report.get('totalStudents', 0)}    "
                f"Present: {report.get('present', 0)}    "
                f"Late: {report.get('late', 0)}    "
                f"Absent: {report.get('absent', 0)}    "
                f"Attendance: {report.get('attendancePercentage', 0)}%"
            )

            summary.setObjectName(
                "sectionTitle"
            )

            layout.addWidget(
                summary
            )

            table = QTableWidget()

            table.setColumnCount(6)

            table.setHorizontalHeaderLabels(
                [
                    "Student Code",
                    "Full Name",
                    "Status",
                    "Check-in Time",
                    "Method",
                    "Remark",
                ]
            )

            table.setRowCount(
                len(records)
            )

            for row, record in enumerate(
                records
            ):

                values = [
                    record.get(
                        "studentCode",
                        "",
                    ),
                    record.get(
                        "fullName",
                        "",
                    ),
                    record.get(
                        "status",
                        "",
                    ),
                    record.get(
                        "checkInTime",
                        "",
                    ),
                    record.get(
                        "method",
                        "",
                    ),
                    record.get(
                        "remark",
                        "",
                    ),
                ]

                for column, value in enumerate(
                    values
                ):

                    item = QTableWidgetItem(
                        str(value)
                    )

                    table.setItem(
                        row,
                        column,
                        item,
                    )

            table.setEditTriggers(
                QTableWidget.NoEditTriggers
            )

            table.setSelectionBehavior(
                QTableWidget.SelectRows
            )

            table.horizontalHeader().setSectionResizeMode(
                1,
                QHeaderView.Stretch,
            )

            layout.addWidget(
                table
            )

            close_button = QPushButton(
                "Close Session"
            )

            close_button.clicked.connect(
                lambda checked=False:
                self.close_session(
                    session_id,
                    dialog,
                )
            )

            layout.addWidget(
                close_button
            )

            dialog.exec()

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Session",
                str(exc),
            )

    # =============================
    # CLOSE SESSION
    # =============================

    def close_session(
        self,
        session_id,
        dialog,
    ):

        answer = QMessageBox.question(
            self,
            "Close Session",
            "Are you sure you want to close this session?",
        )

        if answer != QMessageBox.Yes:
            return

        try:

            self.lecturer_api.close_session(
                session_id
            )

            QMessageBox.information(
                self,
                "Session",
                "Session has been closed successfully.",
            )

            dialog.accept()

            self.refresh()

        except ApiError as exc:

            QMessageBox.warning(
                self,
                "Close Session",
                str(exc),
            )