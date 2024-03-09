from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class HotelItem(Item):
    city_id : str
    name : str
    star : int

    def from_json(json):
        return HotelItem(json["id"], json["city_id"], json["name"], json["star"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "View rooms"

    def description(self) -> str:
        return f"Stars: {self.star}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "city_id" : self.city_id,
            "name" : self.name,
            "star" : self.star
        }

    def set_city_id(self, city_id):
        self.city_id = city_id

    def get_city_id(self):
        return self.city_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_star(self, star):
        self.star = star

    def get_star(self):
        return self.star

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("city_id", WidgetType.Label, self.set_city_id, self.get_city_id),
            DialogLayout("name", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("star", WidgetType.SpinBox, self.set_star, self.get_star)
        ]