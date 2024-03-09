from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class City(db.Model, Model):
    __tablename__ = 'cities'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey('countries.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    hotel = db.relationship("Hotel", backref="city", cascade="all, delete, delete-orphan")

    def __init__(self, id, country_id, name):
        self.id = id
        self.country_id = country_id
        self.name = name

    def __repr__(self) -> str:
        return f"<City {self.id}>"

    def from_args(args):
        return City(Model.get_id(args), args.get("country_id"), args.get("name"))

    def copy(self, other):
        self.id = other.id
        self.country_id = other.country_id
        self.name = other.name

    def json(self) -> dict:
        return {
            "id" : self.id,
            "country_id" : self.country_id,
            "name" : self.name
        }