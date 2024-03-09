from PySide6.QtWidgets import QFrame, QWidget, QLabel, QSizePolicy, QPushButton, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Signal

from gui.shared import general_font, general_bold_font, small_font

from items.item import Item

class ItemWidget(QFrame):

    view_btn_clicked = Signal(Item)
    modify_btn_clicked = Signal(Item)
    remove_btn_clicked = Signal(Item)

    def __init__(self, item, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setFrameStyle(QFrame.Shape.Panel)
        self.setLineWidth(2)

        self.item = None

        self.caption_label = QLabel("Caption")
        self.caption_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.caption_label.setFont(general_bold_font)

        self.view_btn = QPushButton("View")
        self.view_btn.setFont(general_font)
        self.view_btn.clicked.connect(self.on_view_btn_clicked)

        self.modify_btn = QPushButton("Modify")
        self.modify_btn.setFont(general_font)
        self.modify_btn.clicked.connect(self.on_modify_btn_clicked)

        self.remove_btn = QPushButton("Remove")
        self.remove_btn.setFont(general_font)
        self.remove_btn.clicked.connect(self.on_remove_btn_clicked)

        self.description_label = QLabel("Description")
        self.description_label.setFont(small_font)

        self.caption_layout = QHBoxLayout()
        self.caption_layout.addWidget(self.caption_label)
        self.caption_layout.addWidget(self.view_btn)
        self.caption_layout.addWidget(self.modify_btn)
        self.caption_layout.addWidget(self.remove_btn)

        self.description_layout = QHBoxLayout()
        self.description_layout.addSpacing(10)
        self.description_layout.addWidget(self.description_label)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.caption_layout)
        self.main_layout.addLayout(self.description_layout)

        self.set_item(item)

    def set_item(self, item):
        self.item = item

        self.caption_label.setText(item.caption())
        self.view_btn.setText(item.view_btn_caption())
        self.description_label.setText(item.description())

        if len(self.view_btn.text()) == 0:
            self.view_btn.setVisible(False)

    def on_view_btn_clicked(self):
        self.view_btn_clicked.emit(self.item)

    def on_modify_btn_clicked(self):
        self.modify_btn_clicked.emit(self.item)

    def on_remove_btn_clicked(self):
        self.remove_btn_clicked.emit(self.item)