import enum
from app.models.base import db, TimestampMixin


class DocumentType(enum.Enum):
    INE = "INE"
    PASAPORTE = "PASAPORTE"
    LICENCIA = "LICENCIA"


class Visitor(db.Model, TimestampMixin):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))

    # Usamos el Enum definido arriba
    document_type = db.Column(db.Enum(DocumentType), nullable=False)
    document_number = db.Column(db.String(50), nullable=False)

    # Rutas a los archivos
    document_file_path = db.Column(db.String(255))
    face_image_path = db.Column(db.String(255))

    def __repr__(self):
        return f"<Visitor {self.full_name}>"
