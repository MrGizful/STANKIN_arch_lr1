from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Room(db.Model, Model):
    __tablename__ = 'rooms'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hotel_id = db.Column(UUID(as_uuid=True), db.ForeignKey('hotels.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    bed = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    count = db.Column(db.Integer(), nullable=False)
    service_link = db.relationship("RoomServiceLink", backref="room", cascade="all, delete, delete-orphan")

    def __init__(self, id, hotel_id, name, bed, price, count):
        self.id = id
        self.hotel_id = hotel_id
        self.name = name
        self.bed = bed
        self.price = price
        self.count = count

    def __repr__(self) -> str:
        return f"<Room {self.id}>"

    def from_args(args):
        return Room(Model.get_id(args), args.get("hotel_id"), args.get("name"), int(args.get("bed")), float(args.get("price")), int(args.get("count")))

    def copy(self, other):
        self.id = other.id
        self.hotel_id = other.hotel_id
        self.name = other.name
        self.bed = other.bed
        self.price = other.price
        self.count = other.count

    def json(self) -> dict:
        return {
            "id" : self.id,
            "hotel_id" : self.hotel_id,
            "name" : self.name,
            "bed" : self.bed,
            "price" : self.price,
            "count" : self.count
        }