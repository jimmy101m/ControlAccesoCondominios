from app.models.base import db
import uuid


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Quién hizo la acción (FK real porque siempre es un usuario)
    actor_used_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    action = db.Column(
        db.String(100), nullable=False
    )  # Ej: "update_password", "delete_unit"
    entity_type = db.Column(db.String(50), nullable=False)  # Ej: "User", "Invitation"
    entity_id = db.Column(
        db.String(36), nullable=False
    )  # El UUID de la entidad afectada

    # Guardamos el "antes y después" del cambio en formato JSON
    payload = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relación para saber quién fue el responsable
    actor = db.relationship("User")
