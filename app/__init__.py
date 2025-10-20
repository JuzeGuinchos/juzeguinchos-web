from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    from .config import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # cria tabelas em produção (simples)
    with app.app_context():
        db.create_all()

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
