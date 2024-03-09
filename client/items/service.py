from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class ServiceItem(Item):
    name : str
    price : float

    def from_json(json):
        return ServiceItem(json["id"], json["name"], json["price"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return str()

    def description(self) -> str:
        return f"Price: {self.price}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "price" : self.price
        }

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("name", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("price", WidgetType.DoubleSpinBox, self.set_price, self.get_price)
        ]
