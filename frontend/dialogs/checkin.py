from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout


class CheckInDialog(QDialog):
    def __init__(self, parent=None, suggested_session_id=""):
        super().__init__(parent)
        self.setWindowTitle("Submit Attendance")
        self.setMinimumWidth(390)
        layout = QVBoxLayout(self)
        title = QLabel("Attendance check-in")
        title.setObjectName("dialogTitle")
        info = QLabel(
            "Backend hiện tại yêu cầu sessionID khi sinh viên submit.\n"
            "Nhập ID phiên do giảng viên mở và mật khẩu nếu phương thức là PASSWORD."
        )
        info.setWordWrap(True)
        info.setObjectName("muted")
        layout.addWidget(title)
        layout.addWidget(info)

        form = QFormLayout()
        self.session_id = QLineEdit(str(suggested_session_id))
        self.session_id.setPlaceholderText("Ví dụ: 1")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Để trống nếu SELF_SUBMIT")
        self.password.setEchoMode(QLineEdit.Password)
        form.addRow("Session ID", self.session_id)
        form.addRow("Password", self.password)
        layout.addLayout(form)
        submit = QPushButton("SUBMIT ATTENDANCE")
        submit.setObjectName("primaryButton")
        submit.clicked.connect(self.accept)
        layout.addWidget(submit)
