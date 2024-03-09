from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class CityItem(Item):
    country_id : str
    name : str

    def from_json(json):
        return CityItem(json["id"], json["country_id"], json["name"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "View hotels"

    def description(self) -> str:
        return str()

    def params(self) -> dict:
        return {
            "id" : self.id,
            "country_id" : self.country_id,
            "name" : self.name
        }

    def set_country_id(self, country_id):
        self.country_id = country_id

    def get_country_id(self):
        return self.country_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("country_id", WidgetType.Label, self.set_country_id, self.get_country_id),
            DialogLayout("name", WidgetType.LineEdit, self.set_name, self.get_name)
        ]