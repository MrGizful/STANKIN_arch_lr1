import uuid

from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QComboBox
from PySide6.QtCore import Qt

from gui.shared import general_font, header_font

from items.item import WidgetType, DialogLayout

class ItemDialog(QDialog):
    def __init__(self, item, caption, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.item = item

        self.caption_label = QLabel(caption, alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.fields_layout = QGridLayout()
        for dialog_layout in item.dialog_layout():
            row = self.fields_layout.rowCount()

            value_name_layout = DialogLayout(None, WidgetType.Label, lambda *args : None, lambda *args: f"{dialog_layout.param}:")
            self.fields_layout.addWidget(self.widget(value_name_layout), row, 0)
            self.fields_layout.addWidget(self.widget(dialog_layout), row, 1)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFont(general_font)
        self.ok_btn.clicked.connect(self.on_ok_btn_clicked)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFont(general_font)
        self.cancel_btn.clicked.connect(self.on_cancel_btn_clicked)

        self.btns_layout = QHBoxLayout()
        self.btns_layout.addStretch(0)
        self.btns_layout.addWidget(self.ok_btn)
        self.btns_layout.addWidget(self.cancel_btn)
        self.btns_layout.addStretch(0)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addLayout(self.fields_layout)
        self.main_layout.addStretch(0)
        self.main_layout.addLayout(self.btns_layout)

    def widget(self, dialog_layout):
        widget = QWidget()
        value = dialog_layout.get_value_func()

        if dialog_layout.widget_type == WidgetType.Label:
            widget = QLabel()

            if value is not None:
                widget.setText(value)

        if dialog_layout.widget_type == WidgetType.LineEdit:
            widget = QLineEdit()
            widget.textChanged.connect(dialog_layout.set_value_func)

            if value is not None:
                widget.setText(value)

        if dialog_layout.widget_type == WidgetType.SpinBox:
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999999)
            widget.valueChanged.connect(dialog_layout.set_value_func)

            if value is not None:
                widget.setValue(value)

        if dialog_layout.widget_type == WidgetType.DoubleSpinBox:
            widget = QDoubleSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999999)
            widget.setDecimals(2)
            widget.valueChanged.connect(dialog_layout.set_value_func)

            if value is not None:
                widget.setValue(value)

        if dialog_layout.widget_type == WidgetType.ComboBox:
            widget = QComboBox()
            widget.currentTextChanged.connect(dialog_layout.set_value_func)

            if value is not None:
                widget.addItems(value)

        widget.setFont(general_font)
        return widget

    def on_ok_btn_clicked(self):
        if self.item.id is None:
            self.item.id = uuid.uuid4()

        self.accept()

    def on_cancel_btn_clicked(self):
        self.reject()