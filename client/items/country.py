from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class CountryItem(Item):
    name : str

    def from_json(json):
        return CountryItem(json["id"], json["name"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "View cities"

    def description(self) -> str:
        return str()

    def params(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name
        }

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("name", WidgetType.LineEdit, self.set_name, self.get_name)
        ]