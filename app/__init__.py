from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging, os, sys

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    from .config import Config
    app.config.from_object(Config)

    # log básico para stdout (Render captura)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    if not app.logger.handlers:
        app.logger.addHandler(handler)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # HEALTHCHECK - não depende de DB
    @app.route("/healthz")
    def healthz():
        return jsonify(status="ok"), 200

    # tenta criar as tabelas na primeira execução, mas não derruba o app se falhar
    try:
        with app.app_context():
            from . import models  # registra os modelos
            db.create_all()
            app.logger.info("db.create_all() executado com sucesso.")
    except Exception as e:
        app.logger.error(f"Falha ao inicializar o banco: {e}")

    # blueprints
    from .auth import bp as auth_bp
    from .main import bp as main_bp
    from .clientes import bp as clientes_bp
    from .veiculos import bp as veiculos_bp
    from .lancamentos import bp as lanc_bp
    from .importacao import bp as import_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(clientes_bp, url_prefix="/clientes")
    app.register_blueprint(veiculos_bp, url_prefix="/veiculos")
    app.register_blueprint(lanc_bp, url_prefix="/lancamentos")
    app.register_blueprint(import_bp, url_prefix="/importar")

    return app
