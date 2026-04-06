import os
from flask import Flask
from .config import config_map
from .extensions import db, migrate, cors


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
    # Restringir CORS al origen del frontend (configurar CORS_ORIGINS en .env)
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    cors.init_app(app, resources={r"/api/*": {"origins": allowed_origins}})

    # Registrar manejadores de error
    from .errors import register_error_handlers
    register_error_handlers(app)

    # Registrar comandos CLI
    from .commands import register_commands
    register_commands(app)

    return app
