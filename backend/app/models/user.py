from app.models.base import db, BaseMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, BaseMixin):
    __tablename__ = "users"
    full_name = db.Column(db.String(100), nullable=False)
    # 11.1: Índice en email para búsquedas rápidas en el login
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # FK corregida a String(36) para que coincida con el UUID de Role
    role_id = db.Column(db.String(36), db.ForeignKey("roles.id"), nullable=False)

    status = db.Column(db.String(20), default="active")

    invitations = db.relationship("Invitation", back_populates="resident")

    # RELACIÓN BIDIRECCIONAL:
    # Se conecta con 'users' definido en Role
    role = db.relationship("Role", back_populates="users")

    def set_password(self, password):
        # Transforma el texto plano en un hash seguro
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Compara el hash guardado con la contraseña que ingresa el usuario
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"
