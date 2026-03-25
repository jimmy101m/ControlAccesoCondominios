import enum
from app.models.base import db, BaseMixin


class AccessGrantStatus(enum.Enum):
    PENDING_SYNC = "pending_sync"
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"
    USED = "used"
    SYNC_ERROR = "sync_error"


class AccessGrant(db.Model, BaseMixin):
    __tablename__ = "access_grants"
    invitation_id = db.Column(
        db.String(36), db.ForeignKey("invitations.id"), nullable=False
    )
    visitor_id = db.Column(db.String(36), db.ForeignKey("visitors.id"), nullable=False)

    invitation = db.relationship("Invitation", back_populates="grants")
    visitor = db.relationship("Visitor")
    events = db.relationship("AccessEvent", back_populates="grant", cascade="all, delete-orphan")

    status = db.Column(
        db.Enum(AccessGrantStatus), default=AccessGrantStatus.PENDING_SYNC, index=True
    )

    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    single_use = db.Column(db.Boolean, default=True)
    used_at = db.Column(db.DateTime, nullable=True)
    last_synced_at = db.Column(db.DateTime, nullable=True)
