from PySide6.QtWidgets import QWidget, QScrollArea, QSizePolicy, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, Signal

from gui.shared import general_bold_font
from gui.item_widget import ItemWidget

from items.item import Item
from items.country import CountryItem
from items.city import CityItem
from items.hotel import HotelItem
from items.room import RoomItem
from items.service import ServiceItem

from api_request import request

class ItemsContainer(QWidget):

    view_item_changed = Signal(Item)
    modify_btn_clicked = Signal(Item)
    remove_btn_clicked = Signal(Item)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)

        self.inside_widget = QWidget()

        self.no_items_label = QLabel("No items", alignment=Qt.AlignCenter)
        self.no_items_label.setFont(general_bold_font)

        self.inside_layout = QVBoxLayout(self.inside_widget)
        self.inside_layout.addWidget(self.no_items_label, 0, Qt.AlignTop)

        self.scroll_area.setWidget(self.inside_widget)

    def clear(self):
        for i in reversed(range(self.inside_layout.count())):
            widget = self.inside_layout.itemAt(i).widget()

            if type(widget) is not QLabel:
                widget.setParent(None)

        self.no_items_label.setVisible(True)

    def remove_item_widget(self, item_id):
        widget = self.get_item_widget(item_id)

        if widget is None:
            return

        widget.setParent(None)

    def get_item_widget(self, item_id):
        for i in range(self.inside_layout.count()):
            widget = self.inside_layout.itemAt(i).widget()

            if type(widget) is not ItemWidget:
                continue

            if widget.item.id != item_id:
                continue

            return widget

        return None

    def set_items(self, items : list | None):
        if items is None or len(items) == 0:
            self.no_items_label.setVisible(True)
            return

        self.no_items_label.setVisible(False)

        for item in items:
            item_widget = ItemWidget(item)
            item_widget.view_btn_clicked.connect(self.on_view_btn_clicked)
            item_widget.modify_btn_clicked.connect(self.on_modify_btn_clicked)
            item_widget.remove_btn_clicked.connect(self.on_remove_btn_clicked)

            self.inside_layout.addWidget(item_widget, 0, Qt.AlignTop)

        spacer = QWidget()
        spacer.setObjectName("spacer")
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.inside_layout.addWidget(spacer)

    def on_view_btn_clicked(self, item):
        self.view_item_changed.emit(item)

    def on_modify_btn_clicked(self, item):
        self.modify_btn_clicked.emit(item)

    def on_remove_btn_clicked(self, item):
        self.remove_btn_clicked.emit(item)