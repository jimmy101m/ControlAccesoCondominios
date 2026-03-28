from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import (
    authenticate, issue_access_token, serialize_user, revoke_token
)
from app.extensions import db
from app.models.user import User
from app.utils.responses import success_response
from app.errors import ValidationError, UnauthorizedError

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip()
    password = body.get("password", "")

    if not email or not password:
        missing = {}
        if not email:
            missing["email"] = "requerido"
        if not password:
            missing["password"] = "requerido"
        raise ValidationError(missing)

    user = authenticate(email, password)
    token = issue_access_token(user)
    expires_in = int(
        current_app.config["JWT_ACCESS_TOKEN_EXPIRES"].total_seconds()
    )

    return success_response({
        "token": token,
        "token_type": "Bearer",
        "expires_in": expires_in,
        "user": serialize_user(user),
    })


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        raise UnauthorizedError("Usuario no encontrado")
    return success_response({"user": serialize_user(user)})


@auth_bp.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoke_token(jti)
    return success_response({"ok": True, "message": "Sesion cerrada"})
