from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from widgets.sidebar import Sidebar
from widgets.header import Header


class BasePage(QWidget):
    def __init__(
        self,
        title,
        profile,
        navigate,
        logout,
        sidebar_class=None,
    ):
        super().__init__()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---------------------------------
        # SIDEBAR
        # ---------------------------------
        # Student mặc định dùng Sidebar.
        # Lecturer có thể truyền LecturerSidebar
        # thông qua sidebar_class.
        if sidebar_class is None:
            sidebar_class = Sidebar

        sidebar = sidebar_class(profile)

        sidebar.navigate.connect(navigate)
        sidebar.logout_clicked.connect(logout)

        root.addWidget(sidebar)

        # ---------------------------------
        # MAIN BODY
        # ---------------------------------

        self.body = QVBoxLayout()

        self.body.setContentsMargins(
            32,
            28,
            32,
            28,
        )

        self.body.setSpacing(16)

        # Header dùng chung cho Student + Lecturer
        self.body.addWidget(
            Header(
                title,
                profile,
            )
        )

        root.addLayout(self.body)