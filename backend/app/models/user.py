import uuid
from enum import Enum as PyEnum
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class UserRole(PyEnum):
    resident = "resident"
    admin_local = "admin_local"
    guard = "guard"


class UserStatus(PyEnum):
    active = "active"
    inactive = "inactive"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    status = db.Column(db.Enum(UserStatus), nullable=False,
                       default=UserStatus.active)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email} ({self.role.value})>"
