import enum
from app.models.base import db, BaseMixin


class DocumentType(enum.Enum):
    INE = "ine"
    PASAPORTE = "pasaporte"
    LICENCIA = "licencia"


class Visitor(db.Model, BaseMixin):
    __tablename__ = "visitors"
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
