from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class RoomServiceLink(db.Model, Model):
    __tablename__ = 'room_service_links'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = db.Column(UUID(as_uuid=True), db.ForeignKey('rooms.id', ondelete='cascade'), nullable=False, default=uuid.uuid4)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('services.id', ondelete='cascade'), nullable=False, default=uuid.uuid4)

    def __init__(self, id, room_id, service_id):
        self.id = id
        self.room_id = room_id
        self.service_id = service_id

    def __repr__(self) -> str:
        return f"<RoomServiceLink {self.room_id}:{self.service_id}>"

    def from_args(args):
        return RoomServiceLink(Model.get_id(args), args.get("room_id"), args.get("service_id"))

    def copy(self, other):
        self.id = other.id
        self.room_id = other.room_id
        self.service_id = other.service_id

    def json(self) -> dict:
        return {
            "id" : self.id,
            "room_id" : self.room_id,
            "service_id" : self.service_id
        }