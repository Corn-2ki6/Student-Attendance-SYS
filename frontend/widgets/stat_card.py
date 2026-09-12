from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class StatCard(QFrame):
    def __init__(self, title, value="--", subtitle=""):
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        title_label = QLabel(title)
        title_label.setObjectName("muted")
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("statValue")
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("muted")
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(subtitle_label)

    def set_value(self, value):
        self.value_label.setText(str(value))
