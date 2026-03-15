import os
from flask import Flask
from .config import config_map
from .extensions import db, migrate, cors


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__, template_folder="../templates")

    env = env or os.getenv("APP_ENV", "development")
    app.config.from_object(config_map[env])

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Registrar blueprints
    # from .routes.health import health_bp
    # app.register_blueprint(health_bp, url_prefix="/api/v1")

    return app
