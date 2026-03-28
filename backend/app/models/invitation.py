import enum
from app.models.base import db, BaseMixin


class AccesMode(enum.Enum):
    PEDESTRIAN = "pedestrian"
    VEHICLE = "vehicle"


class InvitationStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    REGISTERED = "registered"
    APPROVED = "approved"
    CANCELED = "canceled"
    EXPIRED = "expired"
    USED = "used"

    # investigar manejo de errores de autenticación de archivos


class Invitation(db.Model, BaseMixin):
    __tablename__ = "invitations"

    # FKs usando String(36) por los UUIDs de User
    resident_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    condominium_id = db.Column(
        db.String(36), db.ForeignKey("condominiums.id"), nullable=False
    )
    unit_id = db.Column(db.String(36), db.ForeignKey("units.id"), nullable=False)

    # Campos con Índice para velocidad de búsqueda
    token = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(
        db.Enum(InvitationStatus), default=InvitationStatus.DRAFT, index=True
    )

    acces_mode = db.Column(db.Enum(AccesMode), nullable=False)
    plate_number = db.Column(db.String(20), nullable=True)  # Solo si es vehículo

    expires_at = db.Column(db.DateTime, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    used_at = db.Column(db.DateTime)

    # RELACIONES BIDIRECCIONALES
    # 'resident' permite acceder al User desde la invitación
    resident = db.relationship("User", back_populates="invitations")
    # 'grants' permite ver los permisos generados por esta invitación
    grants = db.relationship(
        "AccessGrant", back_populates="invitation", cascade="all, delete-orphan"
    )
