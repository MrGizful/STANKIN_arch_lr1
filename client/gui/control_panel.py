from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout

from gui.shared import general_font

from PySide6.QtCore import Signal

class ControlPanel(QWidget):

    back_btn_clicked = Signal()
    home_btn_clicked = Signal()
    add_btn_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.back_btn = QPushButton("Back")
        self.back_btn.setFont(general_font)
        self.back_btn.clicked.connect(self.back_btn_clicked.emit)

        self.home_btn = QPushButton("Home")
        self.home_btn.setFont(general_font)
        self.home_btn.clicked.connect(self.home_btn_clicked.emit)

        self.add_btn = QPushButton("Add")
        self.add_btn.setFont(general_font)
        self.add_btn.clicked.connect(self.add_btn_clicked.emit)

        self.main_layout = QHBoxLayout(self)
        self.main_layout.addStretch(0)
        self.main_layout.addWidget(self.back_btn)
        self.main_layout.addWidget(self.home_btn)
        self.main_layout.addWidget(self.add_btn)
        self.main_layout.addStretch(0)