from app.models.base import db, TimestampMixin


class ResidentProfile(db.Model, TimestampMixin):
    __tablename__ = "resident_profiles"

    id = db.Column(db.Integer, primary_key=True)

    # Las tres llaves foráneas del residente
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    condominium_id = db.Column(
        db.Integer, db.ForeignKey("condominiums.id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)

    # El status nos dice si el residente está activo, suspendido o se mudó
    status = db.Column(db.String(20), default="active")

    def __repr__(self):
        return f"<ResidentProfile User {self.user_id} Unit:{self.unit_id}>"
