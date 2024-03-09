from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Service(db.Model, Model):
    __tablename__ = 'services'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    room_link = db.relationship("RoomServiceLink", backref="service", cascade="all, delete, delete-orphan")

    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"<Service {self.id}>"

    def from_args(args):
        return Service(Model.get_id(args), args.get("name"), float(args.get("price")))

    def copy(self, other):
        self.id = other.id
        self.name = other.name
        self.price = other.price

    def json(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "price" : self.price
        }