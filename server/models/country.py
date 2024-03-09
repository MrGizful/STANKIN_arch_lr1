from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Country(db.Model, Model):
    __tablename__ = 'countries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    city = db.relationship("City", backref="country", cascade="all, delete, delete-orphan")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self) -> str:
        return f"<Country {self.id}>"

    def from_args(args):
        return Country(Model.get_id(args), args.get("name"))

    def copy(self, other):
        self.id = other.id
        self.name = other.name
        self.city = other.city

    def json(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name
        }
