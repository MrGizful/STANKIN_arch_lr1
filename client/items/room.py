from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class RoomItem(Item):
    hotel_id : str
    name : str
    bed : int
    price : float
    count : int

    def from_json(json):
        return RoomItem(json["id"], json["hotel_id"], json["name"], json["bed"], json["price"], json["count"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "View services"

    def description(self) -> str:
        return f"Beds: {self.bed}\nPrice: {self.price}\nCount: {self.count}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "hotel_id" : self.hotel_id,
            "name" : self.name,
            "bed" : self.bed,
            "price" : self.price,
            "count" : self.count
        }

    def set_hotel_id(self, hotel_id):
        self.hotel_id = hotel_id

    def get_hotel_id(self):
        return self.hotel_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_bed(self, bed):
        self.bed = bed

    def get_bed(self):
        return self.bed

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def set_count(self, count):
        self.count = count

    def get_count(self):
        return self.count

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("hotel_id", WidgetType.Label, self.set_hotel_id, self.get_hotel_id),
            DialogLayout("name", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("bed", WidgetType.SpinBox, self.set_bed, self.get_bed),
            DialogLayout("price", WidgetType.DoubleSpinBox, self.set_price, self.get_price),
            DialogLayout("count", WidgetType.SpinBox, self.set_count, self.get_count)
        ]