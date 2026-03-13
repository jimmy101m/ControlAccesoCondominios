import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "sqlite:///local_access_node.db"
    )
    LOCAL_API_KEY: str = os.getenv(
        "LOCAL_API_KEY", "local-node-shared-secret"
    )
    FACE_STORAGE_DIR: str = os.getenv(
        "FACE_STORAGE_DIR", "./storage/faces"
    )
    NODE_ID: str = os.getenv("NODE_ID", "condo_pilot_01")
    CORE_CALLBACK_URL: str = os.getenv(
        "CORE_CALLBACK_URL",
        "http://localhost:5000/internal/v1/local-access/events",
    )
    CORE_CALLBACK_API_KEY: str = os.getenv(
        "CORE_CALLBACK_API_KEY", "local-node-shared-secret"
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
