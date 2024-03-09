from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

from enum import Enum

from gui.shared import header_font
from gui.control_panel import ControlPanel
from gui.items_container import ItemsContainer
from gui.home_page_navigation import HomePageNavigation
from gui.item_dialog import ItemDialog

from items.item import Item
from items.country import CountryItem
from items.city import CityItem
from items.hotel import HotelItem
from items.room import RoomItem
from items.service import ServiceItem
from items.service_list import ServiceListItem

from api_request import request

class MainWindow(QWidget):
    class Page(Enum):
        Home = 0
        Countries = 1
        Cities = 2
        Hotels = 3
        Rooms = 4
        Services = 5

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.current_item = None
        self.current_page = MainWindow.Page.Home

        self.caption_label = QLabel("Caption", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.control_panel = ControlPanel()
        self.control_panel.back_btn_clicked.connect(self.on_back_btn_clicked)
        self.control_panel.home_btn_clicked.connect(self.on_home_btn_clicked)
        self.control_panel.add_btn_clicked.connect(self.on_add_btn_clicked)

        self.items_container = ItemsContainer()
        self.items_container.view_item_changed.connect(self.on_view_item_changed)
        self.items_container.modify_btn_clicked.connect(self.on_modify_btn_clicked)
        self.items_container.remove_btn_clicked.connect(self.on_remove_btn_clicked)

        self.home_page_navigation = HomePageNavigation()
        self.home_page_navigation.countries_btn_clicked.connect(self.on_countries_btn_clicked)
        self.home_page_navigation.services_btn_clicked.connect(self.on_services_btn_clicked)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.items_container, 1)
        self.main_layout.addWidget(self.home_page_navigation)
        self.main_layout.addStretch(0)

        self.show_home_page()

    def on_back_btn_clicked(self):
        if self.current_item is None:
            self.show_home_page()
            return

        if self.current_page is MainWindow.Page.Cities:
            self.on_countries_btn_clicked()
            return

        items_func = lambda : None

        if self.current_page is MainWindow.Page.Hotels:
            self.current_item = request.get_country(self.current_item.country_id)
            self.current_page = MainWindow.Page.Cities
            items_func = request.get_cities

        if self.current_page is MainWindow.Page.Rooms:
            self.current_item = request.get_city(self.current_item.city_id)
            self.current_page = MainWindow.Page.Hotels
            items_func = request.get_hotels

        if self.current_page is MainWindow.Page.Services:
            self.current_item = request.get_hotel(self.current_item.hotel_id)
            self.current_page = MainWindow.Page.Rooms
            items_func = request.get_rooms

        self.set_caption(self.current_item.caption())
        self.show_content_page(items_func, self.current_item.id)

    def on_home_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Home
        self.show_home_page()

    def on_add_btn_clicked(self):
        item = Item(None)
        caption = "Add item"
        add_func = lambda *args: False

        if self.current_page is MainWindow.Page.Countries:
            item = CountryItem(None, None)
            caption = "Add country"
            add_func = request.add_country

        if self.current_page is MainWindow.Page.Cities:
            item = CityItem(None, self.current_item.id, None)
            caption = "Add city"
            add_func = request.add_city

        if self.current_page is MainWindow.Page.Hotels:
            item = HotelItem(None, self.current_item.id, None, None)
            caption = "Add hotel"
            add_func = request.add_hotel

        if self.current_page is MainWindow.Page.Rooms:
            item = RoomItem(None, self.current_item.id, None, None, None, None)
            caption = "Add room"
            add_func = request.add_room

        if self.current_page is MainWindow.Page.Services:
            caption = "Add service"

            if self.current_item is None:
                item = ServiceItem(None, None, None)
                add_func = request.add_service
            else:
                service_list = request.get_services_exclude_room(self.current_item.id)
                item = ServiceListItem(self.current_item.id, service_list, None)
                add_func = request.add_room_service

        dialog = ItemDialog(item, caption, self)
        if not dialog.exec():
            return

        if not add_func(dialog.item.params()):
            return

        self.on_view_item_changed(self.current_item)

    def on_countries_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Countries

        self.set_caption("Countries")
        self.show_content_page(request.get_countries)

    def on_services_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Services

        self.set_caption("Services")
        self.show_content_page(request.get_services)

    def on_view_item_changed(self, item):
        self.current_item = item

        if item is None:
            if self.current_page is MainWindow.Page.Countries:
                self.on_countries_btn_clicked()

            if self.current_page is MainWindow.Page.Services:
                self.on_services_btn_clicked()

            return

        items_func = lambda *args: None

        if type(item) is CountryItem:
            self.current_page = MainWindow.Page.Cities
            items_func = request.get_cities

        if type(item) is CityItem:
            self.current_page = MainWindow.Page.Hotels
            items_func = request.get_hotels

        if type(item) is HotelItem:
            self.current_page = MainWindow.Page.Rooms
            items_func = request.get_rooms

        if type(item) is RoomItem:
            self.current_page = MainWindow.Page.Services
            items_func = request.get_services_for_room

        self.set_caption(item.caption())
        self.show_content_page(items_func, item.id)

    def on_modify_btn_clicked(self, item):
        caption = "Modify item"
        modify_func = lambda *args: False

        if self.current_page is MainWindow.Page.Countries:
            caption = "Modify country"
            modify_func = request.modify_country

        if self.current_page is MainWindow.Page.Cities:
            caption = "Modify city"
            modify_func = request.modify_city

        if self.current_page is MainWindow.Page.Hotels:
            caption = "Modify hotel"
            modify_func = request.modify_hotel

        if self.current_page is MainWindow.Page.Rooms:
            caption = "Modify room"
            modify_func = request.modify_room

        if self.current_page is MainWindow.Page.Services:
            caption = "Modify service"
            modify_func = request.modify_service

        dialog = ItemDialog(item, caption, self)
        if not dialog.exec():
            return

        if not modify_func(dialog.item.params()):
            return

        self.on_view_item_changed(self.current_item)

    def on_remove_btn_clicked(self, item):
        delete_success = False

        if type(item) == CountryItem:
            delete_success = request.delete_country(item.id)

        if type(item) == CityItem:
            delete_success = request.delete_city(item.id)

        if type(item) == HotelItem:
            delete_success = request.delete_hotel(item.id)

        if type(item) == RoomItem:
            delete_success = request.delete_room(item.id)

        if type(item) == ServiceItem:
            if self.current_item is None:
                delete_success = request.delete_service(item.id)

            else:
                delete_success = request.delete_room_service(self.current_item.id, item.id)

        if not delete_success:
            return

        self.items_container.remove_item_widget(item.id)

        if self.items_container.inside_layout.count() in [1, 2]:
            self.items_container.clear()

    def show_home_page(self):
        self.control_panel.setVisible(False)
        self.items_container.setVisible(False)
        self.home_page_navigation.setVisible(True)

        self.set_caption("Home page")

    def show_content_page(self, items_func, *args):
        self.control_panel.setVisible(True)
        self.items_container.setVisible(True)
        self.home_page_navigation.setVisible(False)

        self.items_container.clear()
        self.items_container.set_items(items_func(*args))

    def set_caption(self, caption):
        self.caption_label.setText(caption)
