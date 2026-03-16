from app.models.base import db, TimestampMixin


class Unit(db.Model, TimestampMixin):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    unit_number = db.Column(db.String(20), nullable=False)

    # Llave foránea hacia la tabla 'condominiums'
    condominium_id = db.Column(
        db.Integer, db.ForeignKey("condominiums.id"), nullable=False
    )

    # Tip pro: Una relación para acceder al objeto Condominium fácilmente
    condominium = db.relationship("Condominium", backref=db.backref("units", lazy=True))

    def __repr__(self):
        return f"<Unit {self.unit_number} - Condominium {self.condominium_id}>"
