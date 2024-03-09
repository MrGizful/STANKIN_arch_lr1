from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Model:
    def from_args(args):
        return None

    def copy(self, other):
        self.id = other.id

    def get_id(args):
        if args.get("id") is None:
            return uuid.uuid4()

        return args["id"]

    def json(self) -> dict:
        return {}

    def valid(self) -> bool:
        for field in self.json().values():
            if field is None:
                return False

        return True