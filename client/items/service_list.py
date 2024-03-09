from items.item import Item, WidgetType, DialogLayout

class ServiceListItem(Item):
    def __init__(self, id, service_list, current_service) -> None:
        super().__init__(id)
        self.service_list = service_list
        self.current_service = current_service

        if current_service is None and len(service_list) != 0:
            self.current_service = service_list[0]

    def from_json(json):
        return ServiceListItem(json["id"], [])

    def caption(self) -> str:
        return str()

    def view_btn_caption(self) -> str:
        return str()

    def description(self) -> str:
        return str()

    def params(self) -> dict:
        service_id = None
        if self.current_service is not None:
            service_id = self.current_service.id

        return {
            "room_id" : self.id,
            "service_id" : service_id
        }

    def set_current_service(self, current_service_name):
        current_service = self.service_list[0]
        for service in self.service_list:
            if service.name == current_service_name:
                current_service = service

        self.current_service = current_service

    def get_service_list(self):
        return [item.name for item in self.service_list]

    def dialog_layout(self) -> list:
        return [
            DialogLayout("service_list", WidgetType.ComboBox, self.set_current_service, self.get_service_list)
        ]
