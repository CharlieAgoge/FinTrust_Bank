"""Configuration for local vs container runs."""
import os


class Config:
    """Base config."""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("HTTPS") == "1"
    DEBUG = False


class LocalConfig(Config):
    """Local development."""
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
    ENV = "development"


class ContainerConfig(Config):
    """Docker / production-like."""
    ENV = "production"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "container-default-change-in-production"


def get_config():
    if os.environ.get("CONTAINER") == "1" or os.path.exists("/.dockerenv"):
        return ContainerConfig
    return LocalConfig
