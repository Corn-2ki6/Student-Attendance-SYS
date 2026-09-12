from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox


class ChangePasswordDialog(QDialog):
    def __init__(self, student_api, parent=None):
        super().__init__(parent)
        self.api = student_api
        self.setWindowTitle("Change Password")
        self.setMinimumWidth(380)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.current = QLineEdit(); self.current.setEchoMode(QLineEdit.Password)
        self.new = QLineEdit(); self.new.setEchoMode(QLineEdit.Password)
        self.confirm = QLineEdit(); self.confirm.setEchoMode(QLineEdit.Password)
        form.addRow("Current password", self.current)
        form.addRow("New password", self.new)
        form.addRow("Confirm", self.confirm)
        layout.addLayout(form)
        btn = QPushButton("CHANGE PASSWORD")
        btn.setObjectName("primaryButton")
        btn.clicked.connect(self.submit)
        layout.addWidget(btn)

    def submit(self):
        from api.client import ApiError
        if len(self.new.text()) < 6:
            QMessageBox.warning(self, "Invalid", "New password must contain at least 6 characters.")
            return
        if self.new.text() != self.confirm.text():
            QMessageBox.warning(self, "Invalid", "Password confirmation does not match.")
            return
        try:
            self.api.change_password(self.current.text(), self.new.text())
            QMessageBox.information(self, "Success", "Password changed successfully.")
            self.accept()
        except ApiError as exc:
            QMessageBox.warning(self, "Error", str(exc))
