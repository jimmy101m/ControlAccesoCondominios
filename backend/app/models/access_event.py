from app.models.base import db
import uuid


class AccessEvent(db.Model):
    __tablename__ = "access_events"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    acces_grant_id = db.Column(
        db.String(36), db.ForeignKey("access_grants.id"), nullable=False
    )

    source = db.Column(
        db.String(50)
    )  # Ej: "Entrada Principal", "App residente", "Guardia"
    event_type = db.Column(db.String(50))  # Ej: "entrada", "salida"
    result = db.Column(db.String(20))  # Ej: "success", "denied"
    reason = db.Column(db.String(255))  # Ej: "QR Invalido", "Placa no coincide"

    # Usamos db.func.now() para que la base de datos marque la hora exacta del evento
    ocurred_at = db.Column(db.DateTime, default=db.func.now())

    # Este campo guarda el JSON completo que envió el dispositivo (útil para debug)
    raw_payload = db.Column(db.JSON, nullable=True)

    # Relación bidireccional
    grant = db.relationship("AccessGrant", back_populates="events")
