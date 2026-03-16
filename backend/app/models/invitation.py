import enum
from app.models.base import db, TimestampMixin


class AccesMode(enum.Enum):
    PEDESTRIAN = "PEDESTRIAN"
    VEHICLE = "VEHICLE"


class InvitationStatus(enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    REGISTERED = "registered"
    APPROVED = "approved"
    CANCELED = "canceled"
    EXPIRED = "expired"
    USED = "used"


class Invitation(db.Model, TimestampMixin):
    __tablename__ = "invitations"

    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    condominium_id = db.Column(
        db.Integer, db.ForeignKey("condominiums.id"), nullable=False
    )
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)

    token = db.Column(db.String(100), unique=True, nullable=False)
    acces_mode = db.Column(db.Enum(AccesMode), nullable=False)
    plate_number = db.Column(db.String(20), nullable=True)  # Solo si es vehículo

    status = db.Column(db.Enum(InvitationStatus), default=InvitationStatus.DRAFT)

    expires_at = db.Column(db.DateTime, nullable=False)
    confirmed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    used_at = db.Column(db.DateTime)
