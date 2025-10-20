import os

# Pega a URL do banco de dados do ambiente (Render). Se não tiver, usa SQLite local.
URI = os.getenv("DATABASE_URL", "sqlite:///local.db")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Se estiver usando SQLite, desabilita a checagem de thread para rodar bem no Gunicorn
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"connect_args": {"check_same_thread": False}}
        if URI.startswith("sqlite")
        else {}
    )
