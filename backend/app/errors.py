import logging
from flask import jsonify

logger = logging.getLogger(__name__)


class AppError(Exception):
    code: str = "INTERNAL_ERROR"
    status_code: int = 400
    default_message: str = "Error"

    def __init__(self, message: str | None = None, details: dict | None = None):
        super().__init__()
        self.message = message or self.__class__.default_message
        self.details = details or {}

    def to_dict(self):
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
            }
        }


class ValidationError(AppError):
    code = "VALIDATION_ERROR"
    status_code = 400
    default_message = "Error de validacion"

    def __init__(self, details: dict | None = None):
        super().__init__(message=self.default_message, details=details)


class UnauthorizedError(AppError):
    code = "UNAUTHORIZED"
    status_code = 401
    default_message = "No autorizado"


class ForbiddenError(AppError):
    code = "FORBIDDEN"
    status_code = 403
    default_message = "Acceso denegado"


class NotFoundError(AppError):
    code = "NOT_FOUND"
    status_code = 404
    default_message = "Recurso no encontrado"

    def __init__(self, resource: str = "Recurso"):
        super().__init__(message=f"{resource} no encontrado")


class ConflictError(AppError):
    code = "CONFLICT"
    status_code = 409
    default_message = "Conflicto"

    def __init__(self, resource: str = "Recurso"):
        super().__init__(message=f"{resource} ya existe")


class BusinessRuleError(AppError):
    code = "BUSINESS_RULE_ERROR"
    status_code = 422
    default_message = "Regla de negocio violada"


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(e):
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": {"code": "BAD_REQUEST", "message": "Solicitud invalida", "details": {}}}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Autenticacion requerida", "details": {}}}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"error": {"code": "FORBIDDEN", "message": "Acceso denegado", "details": {}}}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Recurso no encontrado", "details": {}}}), 404

    @app.errorhandler(409)
    def conflict(e):
        return jsonify({"error": {"code": "CONFLICT", "message": "Conflicto", "details": {}}}), 409

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({"error": {"code": "BUSINESS_RULE_ERROR", "message": "Entidad no procesable", "details": {}}}), 422

    @app.errorhandler(500)
    def internal(e):
        logger.exception(e)
        return jsonify({"error": {"code": "INTERNAL_ERROR", "message": "Error interno del servidor", "details": {}}}), 500
