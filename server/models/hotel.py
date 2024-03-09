from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Hotel(db.Model, Model):
    __tablename__ = 'hotels'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey('cities.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    star = db.Column(db.Integer(), nullable=False)
    room = db.relationship("Room", backref="hotel", cascade="all, delete, delete-orphan")

    def __init__(self, id, city_id, name, star):
        self.id = id
        self.city_id = city_id
        self.name = name
        self.star = star

    def __repr__(self) -> str:
        return f"<Hotel {self.id}>"

    def from_args(args):
        return Hotel(Model.get_id(args), args.get("city_id"), args.get("name"), int(args.get("star")))

    def copy(self, other):
        self.id = other.id
        self.city_id = other.city_id
        self.name = other.name
        self.star = other.star
        self.room = other.room

    def json(self) -> dict:
        return {
            "id" : self.id,
            "city_id" : self.city_id,
            "name" : self.name,
            "star" : self.star
        }