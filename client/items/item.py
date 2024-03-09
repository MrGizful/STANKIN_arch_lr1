from dataclasses import dataclass
from enum import Enum
from typing import Callable

class WidgetType(Enum):
        Label = 0
        LineEdit = 1
        SpinBox = 2
        DoubleSpinBox = 3
        ComboBox = 4
        Widget = 5

class DialogLayout:
    def __init__(self, param, widget_type, set_value_func, get_value_func) -> None:
        self.param = param
        self.widget_type = widget_type
        self.set_value_func = set_value_func
        self.get_value_func = get_value_func

@dataclass
class Item:
    id : str

    def from_json(json):
        return Item(json["id"])

    def caption(self) -> str:
        return str()

    def view_btn_caption(self) -> str:
        return str()

    def description(self) -> str:
        return str()

    def params(self) -> dict:
        return {
            "id" : self.id
        }

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def dialog_layout(self) -> list:
        return [
            DialogLayout("id", Item.WidgetType.Label, self.set_id, self.get_id)
        ]