from flask import Flask, jsonify, request

import uuid

from models.shared import Model, db
from models.country import Country
from models.city import City
from models.hotel import Hotel
from models.room_service_link import RoomServiceLink
from models.room import Room
from models.service import Service

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost:5432/booking"

db.init_app(app)
with app.app_context():
    db.create_all()

def get_list(type, **kargs):
    query = type.query.filter_by(**kargs).all()
    return jsonify([item.json() for item in query])

def get_item(type, **kargs):
    query = type.query.filter_by(**kargs).first()
    if query is None:
        return jsonify(None), 404

    return jsonify(query.json())

def add_item(type):
    item = type.from_args(request.args)
    if not item.valid():
        return jsonify(), 400

    db.session.add(item)
    db.session.commit()

    return jsonify()

def modify_item(type):
    new_item = type.from_args(request.args)
    if not new_item.valid():
        return jsonify(), 400

    current_item = type.query.filter_by(id=new_item.id).first()
    if current_item is None:
        return jsonify(), 400

    current_item.copy(new_item)
    db.session.commit()

    return jsonify()

def delete_item(type, **kargs):
    delete_count = type.query.filter_by(**kargs).delete()
    db.session.commit()

    if delete_count == 0:
        return jsonify(), 404
    
    return jsonify()

@app.route("/countries", methods=['GET'])
def countries():
    return get_list(Country)

@app.route("/country/<contry_id>", methods=['GET'])
def country(contry_id):
    return get_item(Country, id=contry_id)

@app.route("/country/add", methods=['POST'])
def country_add():
    return add_item(Country)

@app.route("/country/modify", methods=['POST'])
def country_modify():
    return modify_item(Country)

@app.route("/country/delete/<contry_id>", methods=['DELETE'])
def country_delete(contry_id):
    return delete_item(Country, id=contry_id)

@app.route("/cities/<country_id>", methods=['GET'])
def cities(country_id):
    return get_list(City, country_id=country_id)

@app.route("/city/<city_id>", methods=['GET'])
def city(city_id):
    return get_item(City, id=city_id)

@app.route("/city/add", methods=['POST'])
def city_add():
    return add_item(City)

@app.route("/city/modify", methods=['POST'])
def city_modify():
    return modify_item(City)

@app.route("/city/delete/<city_id>", methods=['DELETE'])
def city_delete(city_id):
    return delete_item(City, id=city_id)

@app.route("/hotels/<city_id>", methods=['GET'])
def hotels(city_id):
    return get_list(Hotel, city_id=city_id)

@app.route("/hotel/<hotel_id>", methods=['GET'])
def hotel(hotel_id):
    return get_item(Hotel, id=hotel_id)

@app.route("/hotel/add", methods=['POST'])
def hotel_add():
    return add_item(Hotel)

@app.route("/hotel/modify", methods=['POST'])
def hotel_modify():
    return modify_item(Hotel)

@app.route("/hotel/delete/<hotel_id>", methods=['DELETE'])
def hotel_delete(hotel_id):
    return delete_item(Hotel, id=hotel_id)

@app.route("/rooms/<hotel_id>", methods=['GET'])
def rooms(hotel_id):
    return get_list(Room, hotel_id=hotel_id)

@app.route("/room/<room_id>", methods=['GET'])
def room(room_id):
    return get_item(Room, id=room_id)

@app.route("/room/add", methods=['POST'])
def room_add():
    return add_item(Room)

@app.route("/room/modify", methods=['POST'])
def room_modify():
    return modify_item(Room)

@app.route("/room/add-service", methods=['POST'])
def room_add_service():
    room_service_link = RoomServiceLink.from_args(request.args)
    if not room_service_link.valid():
        return jsonify(), 400

    existed_link_query = RoomServiceLink.query \
        .filter_by(room_id=room_service_link.room_id, service_id=room_service_link.service_id) \
        .all()

    if len(existed_link_query) != 0:
        return jsonify(), 404

    db.session.add(room_service_link)
    db.session.commit()

    return jsonify()

@app.route("/room/delete/<room_id>", methods=['DELETE'])
def room_delete(room_id):
    return delete_item(Room, id=room_id)

@app.route("/room/<room_id>/delete-service/<service_id>", methods=['DELETE'])
def room_delete_service(room_id, service_id):
    return delete_item(RoomServiceLink, room_id=room_id, service_id=service_id)

@app.route("/services", methods=['GET'])
def services():
    return get_list(Service)

@app.route("/services/<room_id>", methods=['GET'])
def services_by_room_id(room_id):
    service_ids_query = RoomServiceLink.query.filter_by(room_id=room_id).all()
    service_ids = [link.service_id for link in service_ids_query]

    type = request.args.get("type")
    if type not in ["include", "exclude"]:
        return jsonify(), 400
    
    filter = Service.id.in_(service_ids) if type == "include" else ~Service.id.in_(service_ids)
    return jsonify([service.json() for service in Service.query.filter(filter).all()])

@app.route("/service/add", methods=['POST'])
def service_add():
    return add_item(Service)

@app.route("/service/modify", methods=['POST'])
def service_modify():
    return modify_item(Service)

@app.route("/service/delete/<service_id>", methods=['DELETE'])
def service_delete(service_id):
    return delete_item(Service, id=service_id)

if __name__ == "__main__":
    app.run()