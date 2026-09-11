from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)

from pages.base import BasePage
from widgets.lecturer_sidebar import LecturerSidebar


class LecturerClassesPage(BasePage):
    def __init__(self, profile, navigate, logout, lecturer_api):
        super().__init__(
            "My Classes",
            profile,
            navigate,
            logout,
            sidebar_class=LecturerSidebar,
        )

        self.profile = profile
        self.lecturer_api = lecturer_api

        self.classes_data = []
        self.students_data = []

        self.build_ui()

    def build_ui(self):
        title = QLabel("My Classes")
        title.setObjectName("pageTitle")
        self.body.addWidget(title)

        description = QLabel(
            "View the classes assigned to you and their enrolled students."
        )
        description.setObjectName("muted")
        self.body.addWidget(description)

        # Class selector
        filter_card = QFrame()
        filter_card.setObjectName("card")

        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(20, 16, 20, 16)
        filter_layout.setSpacing(12)

        class_label = QLabel("Class:")
        class_label.setObjectName("muted")

        self.class_combo = QComboBox()
        self.class_combo.setMinimumWidth(450)
        self.class_combo.currentIndexChanged.connect(
            self.on_class_changed
        )

        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("primaryButton")
        refresh_button.setCursor(Qt.PointingHandCursor)
        refresh_button.clicked.connect(self.refresh)

        filter_layout.addWidget(class_label)
        filter_layout.addWidget(self.class_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(refresh_button)

        self.body.addWidget(filter_card)

        # Class information
        self.class_info = QLabel("No class selected.")
        self.class_info.setObjectName("sectionTitle")
        self.class_info.setWordWrap(True)

        self.body.addWidget(self.class_info)

        # Student table
        self.table = QTableWidget()
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "Student Code",
                "Full Name",
                "Email",
                "Enrollment ID",
                "Status",
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

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents,
        )

        self.body.addWidget(self.table)

    # =====================================================
    # LOAD CLASSES
    # =====================================================

    def refresh(self):
        try:
            classes = self.lecturer_api.classes()

            if classes is None:
                classes = []

            self.classes_data = classes

            current_class_id = self.class_combo.currentData()

            self.class_combo.blockSignals(True)
            self.class_combo.clear()

            if not self.classes_data:
                self.class_combo.addItem(
                    "No classes assigned"
                )

                self.class_combo.setEnabled(False)

                self.class_info.setText(
                    "You have not been assigned to any classes."
                )

                self.table.setRowCount(0)

                self.class_combo.blockSignals(False)
                return

            self.class_combo.setEnabled(True)

            selected_index = 0

            for index, class_item in enumerate(
                self.classes_data
            ):
                class_id = class_item.get("classID")

                class_code = class_item.get(
                    "classCode",
                    "Unknown Class",
                )

                course_code = class_item.get(
                    "courseCode",
                    "",
                )

                course_name = class_item.get(
                    "courseName",
                    "",
                )

                text = class_code

                if course_code:
                    text += f" - {course_code}"

                if course_name:
                    text += f" - {course_name}"

                self.class_combo.addItem(
                    text,
                    class_id,
                )

                if (
                    current_class_id is not None
                    and class_id == current_class_id
                ):
                    selected_index = index

            self.class_combo.setCurrentIndex(
                selected_index
            )

            self.class_combo.blockSignals(False)

            self.load_students()

        except Exception as exc:
            self.class_combo.blockSignals(False)

            self.classes_data = []
            self.students_data = []

            self.class_combo.clear()
            self.class_combo.setEnabled(False)

            self.table.setRowCount(0)

            self.class_info.setText(
                "Unable to load classes."
            )

            QMessageBox.warning(
                self,
                "Load Error",
                f"Unable to load your classes.\n\n{exc}",
            )

    # =====================================================
    # CLASS CHANGED
    # =====================================================

    def on_class_changed(self, index):
        if index < 0:
            return

        class_id = self.class_combo.itemData(index)

        if class_id is None:
            self.table.setRowCount(0)
            return

        self.load_students()

    # =====================================================
    # LOAD STUDENTS
    # =====================================================

    def load_students(self):
        index = self.class_combo.currentIndex()

        if index < 0:
            self.table.setRowCount(0)
            return

        class_id = self.class_combo.itemData(index)

        if class_id is None:
            self.table.setRowCount(0)
            return

        try:
            selected_class = None

            for class_item in self.classes_data:
                if class_item.get("classID") == class_id:
                    selected_class = class_item
                    break

            if selected_class is None:
                self.class_info.setText(
                    "Class information is unavailable."
                )
                self.table.setRowCount(0)
                return

            self.update_class_info(
                selected_class
            )

            students = self.lecturer_api.class_students(
                class_id
            )

            if students is None:
                students = []

            self.students_data = students

            self.populate_table()

        except Exception as exc:
            self.students_data = []

            self.table.setRowCount(0)

            self.class_info.setText(
                "Unable to load students."
            )

            QMessageBox.warning(
                self,
                "Load Error",
                f"Unable to load students for this class.\n\n{exc}",
            )

    # =====================================================
    # CLASS INFORMATION
    # =====================================================

    def update_class_info(self, class_item):
        class_code = class_item.get(
            "classCode",
            "Unknown Class",
        )

        course_code = class_item.get(
            "courseCode",
            "",
        )

        course_name = class_item.get(
            "courseName",
            "",
        )

        semester = class_item.get(
            "semester",
            "",
        )

        academic_year = class_item.get(
            "academicYear",
            "",
        )

        credits = class_item.get(
            "credits",
            "",
        )

        parts = [class_code]

        if course_code:
            parts.append(course_code)

        if course_name:
            parts.append(course_name)

        if semester:
            parts.append(
                f"Semester {semester}"
            )

        if academic_year:
            parts.append(
                f"Academic Year {academic_year}"
            )

        if credits:
            parts.append(
                f"{credits} Credits"
            )

        self.class_info.setText(
            " • ".join(
                str(part)
                for part in parts
                if part
            )
        )

    # =====================================================
    # POPULATE STUDENT TABLE
    # =====================================================

    def populate_table(self):
        self.table.clearContents()

        self.table.setRowCount(
            len(self.students_data)
        )

        if not self.students_data:
            current_text = self.class_info.text()

            if "No students enrolled" not in current_text:
                self.class_info.setText(
                    f"{current_text}  •  No students enrolled."
                )

            return

        for row, student in enumerate(
            self.students_data
        ):
            student_code = student.get(
                "studentCode",
                "",
            )

            full_name = student.get(
                "fullName",
                "",
            )

            email = student.get(
                "email",
                "",
            )

            enrollment_id = student.get(
                "enrollmentID",
                "",
            )

            enrollment_status = student.get(
                "enrollmentStatus",
                "",
            )

            values = [
                student_code,
                full_name,
                email,
                (
                    str(enrollment_id)
                    if enrollment_id is not None
                    else ""
                ),
                enrollment_status,
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(
                    str(value)
                )

                if column in (0, 3, 4):
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                self.table.setItem(
                    row,
                    column,
                    item,
                )