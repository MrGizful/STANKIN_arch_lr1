import requests

from items.country import CountryItem
from items.city import CityItem
from items.hotel import HotelItem
from items.room import RoomItem
from items.service import ServiceItem

class APIRequest:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_list(type, url, **kargs):
        response = requests.get(url, **kargs)

        if response.status_code != 200:
            return None

        return [type.from_json(item) for item in response.json()]

    def get_item(type, url):
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return type.from_json(response.json())

    def post_item(url, params):
        response = requests.post(url, params=params)
        return response.status_code == 200

    def delete_item(url):
        response = requests.delete(url)
        return response.status_code == 200

    def get_countries(self):
        url = f"{self.base_url}/countries"
        return APIRequest.get_list(CountryItem, url)

    def get_country(self, country_id):
        url = f"{self.base_url}/country/{country_id}"
        return APIRequest.get_item(CountryItem, url)

    def add_country(self, params):
        url = f"{self.base_url}/country/add"
        return APIRequest.post_item(url, params)

    def modify_country(self, params):
        url = f"{self.base_url}/country/modify"
        return APIRequest.post_item(url, params)

    def delete_country(self, country_id):
        url = f"{self.base_url}/country/delete/{country_id}"
        return APIRequest.delete_item(url)

    def get_cities(self, country_id):
        url = f"{self.base_url}/cities/{country_id}"
        return APIRequest.get_list(CityItem, url)

    def get_city(self, city_id):
        url = f"{self.base_url}/city/{city_id}"
        return APIRequest.get_item(CityItem, url)

    def add_city(self, params):
        url = f"{self.base_url}/city/add"
        return APIRequest.post_item(url, params)

    def modify_city(self, params):
        url = f"{self.base_url}/city/modify"
        return APIRequest.post_item(url, params)

    def delete_city(self, city_id):
        url = f"{self.base_url}/city/delete/{city_id}"
        return APIRequest.delete_item(url)

    def get_hotels(self, city_id):
        url = f"{self.base_url}/hotels/{city_id}"
        return APIRequest.get_list(HotelItem, url)

    def get_hotel(self, hotel_id):
        url = f"{self.base_url}/hotel/{hotel_id}"
        return APIRequest.get_item(HotelItem, url)

    def add_hotel(self, params):
        url = f"{self.base_url}/hotel/add"
        return APIRequest.post_item(url, params)

    def modify_hotel(self, params):
        url = f"{self.base_url}/hotel/modify"
        return APIRequest.post_item(url, params)

    def delete_hotel(self, hotel_id):
        url = f"{self.base_url}/hotel/delete/{hotel_id}"
        return APIRequest.delete_item(url)

    def get_rooms(self, hotel_id):
        url = f"{self.base_url}/rooms/{hotel_id}"
        return APIRequest.get_list(RoomItem, url)

    def get_room(self, room_id):
        url = f"{self.base_url}/room/{room_id}"
        return APIRequest.get_item(RoomItem, url)

    def add_room(self, params):
        url = f"{self.base_url}/room/add"
        return APIRequest.post_item(url, params)

    def modify_room(self, params):
        url = f"{self.base_url}/room/modify"
        return APIRequest.post_item(url, params)

    def add_room_service(self, params):
        url = f"{self.base_url}/room/add-service"
        return APIRequest.post_item(url, params)

    def delete_room(self, room_id):
        url = f"{self.base_url}/room/delete/{room_id}"
        return APIRequest.delete_item(url)

    def delete_room_service(self, room_id, service_id):
        url = f"{self.base_url}/room/{room_id}/delete-service/{service_id}"
        return APIRequest.delete_item(url)

    def get_services(self):
        url = f"{self.base_url}/services"
        return APIRequest.get_list(ServiceItem, url)

    def get_services_for_room(self, room_id):
        url = f"{self.base_url}/services/{room_id}"
        params = { "type" : "include" }
        return APIRequest.get_list(ServiceItem, url, params=params)

    def get_services_exclude_room(self, room_id):
        url = f"{self.base_url}/services/{room_id}"
        params = { "type" : "exclude" }
        return APIRequest.get_list(ServiceItem, url, params=params)

    def add_service(self, params):
        url = f"{self.base_url}/service/add"
        return APIRequest.post_item(url, params)

    def modify_service(self, params):
        url = f"{self.base_url}/service/modify"
        return APIRequest.post_item(url, params)

    def delete_service(self, service_id):
        url = f"{self.base_url}/service/delete/{service_id}"
        return APIRequest.delete_item(url)

request = APIRequest()