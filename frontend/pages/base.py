from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from widgets.sidebar import Sidebar
from widgets.header import Header


class BasePage(QWidget):
    def __init__(self, title, profile, navigate, logout):
        super().__init__()
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = Sidebar(profile)
        sidebar.navigate.connect(navigate)
        sidebar.logout_clicked.connect(logout)
        root.addWidget(sidebar)

        self.body = QVBoxLayout()
        self.body.setContentsMargins(32, 28, 32, 28)
        self.body.setSpacing(16)
        self.body.addWidget(Header(title, profile))
        root.addLayout(self.body)
