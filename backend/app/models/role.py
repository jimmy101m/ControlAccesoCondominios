from app.models.base import db, BaseMixin


class Role(db.Model, BaseMixin):
    __tablename__ = "roles"

    # El 'id', 'created_at' y 'updated_at' ya vienen en BaseMixin
    name = db.Column(db.String(50), unique=True, nullable=False)

    # RELACIÓN BIDIRECCIONAL:
    # 'users' nos permite hacer: mi_rol.users para ver a todos los que tienen este rol.
    # back_populates debe coincidir con el nombre del atributo en el modelo User.

    users = db.relationship("User", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Role {self.name}>"
