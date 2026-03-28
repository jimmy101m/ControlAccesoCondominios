from app.models.base import db, TimestampMixin


class Condominium(db.Model, TimestampMixin):
    __tablename__ = "condominiums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="active")

    def __repr__(self):
        return f"<Condominium {self.name}>"
