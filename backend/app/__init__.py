import os
from flask import Flask
from .config import config_map
from .extensions import db, migrate, jwt, cors


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)

    env = env or os.getenv("APP_ENV", "development")
    app.config.from_object(config_map[env])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Registrar blueprints
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # Registrar comandos CLI
    from .commands import register_commands
    register_commands(app)

    return app
