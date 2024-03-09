from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal

from gui.shared import general_font

class HomePageNavigation(QWidget):

    countries_btn_clicked = Signal()
    services_btn_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.countries_btn = QPushButton("Countries")
        self.countries_btn.setFixedWidth(100)
        self.countries_btn.setFont(general_font)
        self.countries_btn.clicked.connect(self.countries_btn_clicked)

        self.services_btn = QPushButton("Services")
        self.services_btn.setFixedWidth(100)
        self.services_btn.setFont(general_font)
        self.services_btn.clicked.connect(self.services_btn_clicked)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.countries_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.services_btn, 0, Qt.AlignmentFlag.AlignHCenter)