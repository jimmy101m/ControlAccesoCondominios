import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "sqlite:///dev.db"
    )
    FILES_ROOT: str = os.getenv("FILES_ROOT", "./storage")
    FACE_UPLOAD_DIR: str = os.getenv("FACE_UPLOAD_DIR", "./storage/faces")
    DOCUMENT_UPLOAD_DIR: str = os.getenv(
        "DOCUMENT_UPLOAD_DIR", "./storage/documents"
    )
    LOCAL_NODE_BASE_URL: str = os.getenv(
        "LOCAL_NODE_BASE_URL", "http://localhost:5500"
    )
    LOCAL_NODE_API_KEY: str = os.getenv(
        "LOCAL_NODE_API_KEY", "local-node-shared-secret"
    )
    WHATSAPP_SUPPORT_NUMBER: str = os.getenv(
        "WHATSAPP_SUPPORT_NUMBER", "521XXXXXXXXXX"
    )


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class TestingConfig(BaseConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


config_map: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
