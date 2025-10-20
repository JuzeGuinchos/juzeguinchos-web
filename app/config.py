import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Ajuste de engine: pre_ping e check_same_thread no sqlite
    _URL = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://")
    SQLALCHEMY_DATABASE_URI = _URL
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"pool_pre_ping": True, "connect_args": {"check_same_thread": False}}
        if _URL.startswith("sqlite")
        else {"pool_pre_ping": True}
    )
