from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
)

from pages.base import BasePage
from widgets.lecturer_sidebar import LecturerSidebar


class LecturerDashboardPage(BasePage):
    def __init__(self, profile, navigate, logout, lecturer_api):
        super().__init__(
            "Lecturer Dashboard",
            profile,
            navigate,
            logout,
            sidebar_class=LecturerSidebar,
        )

        self.profile = profile
        self.lecturer_api = lecturer_api

        self.build_ui()

    def build_ui(self):
        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        self.body.addWidget(title)

        # =========================
        # Statistics
        # =========================

        cards = QHBoxLayout()
        cards.setSpacing(16)

        self.classes_card = self.create_stat_card(
            "My Classes",
            "0",
        )

        self.sessions_card = self.create_stat_card(
            "Attendance Sessions",
            "0",
        )

        self.students_card = self.create_stat_card(
            "Students",
            "0",
        )

        cards.addWidget(self.classes_card)
        cards.addWidget(self.sessions_card)
        cards.addWidget(self.students_card)

        self.body.addLayout(cards)

        # =========================
        # Welcome section
        # =========================

        welcome = QFrame()
        welcome.setObjectName("card")

        welcome_layout = QVBoxLayout(welcome)
        welcome_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        welcome_title = QLabel(
            "Welcome to Lecturer Attendance System"
        )
        welcome_title.setObjectName("sectionTitle")

        self.welcome_text = QLabel(
            "Loading lecturer information..."
        )
        self.welcome_text.setObjectName("muted")
        self.welcome_text.setWordWrap(True)

        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(self.welcome_text)

        self.body.addWidget(welcome)

        self.body.addStretch()

    def create_stat_card(self, title, value):
        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        title_label = QLabel(title)
        title_label.setObjectName("muted")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.value_label = value_label

        return card

    def refresh(self):
        try:
            # =========================
            # Lecturer profile
            # =========================

            profile = self.lecturer_api.profile()

            full_name = profile.get(
                "fullName",
                "Lecturer",
            )

            lecturer_code = profile.get(
                "lecturerCode",
                "",
            )

            department = profile.get(
                "department",
                "",
            )

            self.welcome_text.setText(
                f"Hello {full_name} "
                f"({lecturer_code}).\n"
                f"Department: {department}"
            )

            # =========================
            # Classes
            # =========================

            classes = self.lecturer_api.classes()

            if classes is None:
                classes = []

            self.classes_card.value_label.setText(
                str(len(classes))
            )

            # =========================
            # Attendance sessions
            # =========================

            sessions = self.lecturer_api.sessions()

            if sessions is None:
                sessions = []

            self.sessions_card.value_label.setText(
                str(len(sessions))
            )

            # =========================
            # Students
            # =========================

            student_ids = set()

            for class_item in classes:
                class_id = class_item.get(
                    "classID"
                )

                if class_id is None:
                    continue

                try:
                    students = (
                        self.lecturer_api.class_students(
                            class_id
                        )
                    )

                    if students is None:
                        continue

                    for student in students:
                        student_id = student.get(
                            "studentID"
                        )

                        if student_id is not None:
                            student_ids.add(
                                student_id
                            )

                except Exception:
                    # Keep the dashboard running
                    # if one class cannot be loaded.
                    continue

            self.students_card.value_label.setText(
                str(len(student_ids))
            )

        except Exception as exc:
            self.welcome_text.setText(
                "Unable to load lecturer information.\n"
                f"{exc}"
            )