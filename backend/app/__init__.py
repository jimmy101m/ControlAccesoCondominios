import os
from flask import Flask
from .config import config_map
from .extensions import db, migrate, jwt, cors


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)

    env = env or os.getenv("APP_ENV", "development")
    cfg = config_map[env]

    # Validar secretos en produccion
    if env == "production":
        cfg.validate_secrets()

    app.config.from_object(cfg)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    # Restringir CORS al origen del frontend (configurar CORS_ORIGINS en .env)
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    cors.init_app(app, resources={r"/api/*": {"origins": allowed_origins}})

    # Registrar manejadores de error
    from .errors import register_error_handlers
    register_error_handlers(app)

    # Callbacks JWT
    _register_jwt_callbacks(app)

    # Registrar blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # Registrar comandos CLI
    from .commands import register_commands
    register_commands(app)

    return app


def _register_jwt_callbacks(app: Flask) -> None:
    from .services.auth_service import is_token_revoked
    from .utils.responses import error_response

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("TOKEN_EXPIRED", "El token ha expirado", status=401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return error_response("INVALID_TOKEN", "Token invalido", status=401)

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return error_response("UNAUTHORIZED", "Token requerido", status=401)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_payload)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return error_response("TOKEN_REVOKED", "Token revocado", status=401)
