from flask_jwt_extended import create_access_token
from app.models.user import User
from app.errors import UnauthorizedError

# MVP in-memory blocklist — lost on restart, acceptable for MVP
_token_blocklist: set[str] = set()


def authenticate(email: str, password: str) -> User:
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        raise UnauthorizedError("Credenciales invalidas")
    if user.status != "active":
        raise UnauthorizedError("Usuario inactivo")
    return user


def issue_access_token(user: User) -> str:
    return create_access_token(identity=user.id)


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role.name,
        "status": user.status,
    }


def revoke_token(jti: str) -> None:
    _token_blocklist.add(jti)


def is_token_revoked(jwt_payload: dict) -> bool:
    return jwt_payload.get("jti") in _token_blocklist
