from app import create_app, db
from flask_migrate import Migrate
from app.models import User, Cliente, Veiculo, Lancamento

app = create_app()
migrate = Migrate(app, db)

# Para gerar migrações:
#   flask db init
#   flask db migrate -m "init"
#   flask db upgrade
