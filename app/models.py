from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db, login_manager

# ==== Usuários (login) ====
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id): return User.query.get(int(user_id))

# ==== Clientes ====
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(18), unique=True, index=True)
    razao_social = db.Column(db.String(255))
    nome_fantasia = db.Column(db.String(255))
    cep = db.Column(db.String(20))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(50))
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    municipio = db.Column(db.String(255))
    uf = db.Column(db.String(2))
    telefone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    inscricao_estadual = db.Column(db.String(50))
    observacoes = db.Column(db.Text)

    def __repr__(self): return f"<Cliente {self.cnpj} {self.razao_social}>"

# ==== Veículos ====
class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), unique=True, index=True)
    modelo = db.Column(db.String(255))
    marca = db.Column(db.String(255))
    ano = db.Column(db.String(10))
    renavam = db.Column(db.String(50))
    chassi = db.Column(db.String(50))
    proprietario = db.Column(db.String(255))
    observacoes = db.Column(db.Text)

    def __repr__(self): return f"<Veiculo {self.placa}>"

# ==== Lançamentos de caixa ====
class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(20))                 # 'ENTRADA' | 'SAIDA'
    cliente = db.Column(db.String(255))             # nome/razão
    cnpj = db.Column(db.String(18))
    veiculo = db.Column(db.String(255))
    placa = db.Column(db.String(10))
    descricao = db.Column(db.String(255))
    categoria = db.Column(db.String(100))
    valor = db.Column(db.Numeric(12,2))
    origem = db.Column(db.String(255))
    destino = db.Column(db.String(255))
    cidade_despesa = db.Column(db.String(255))
    competencia = db.Column(db.String(7), index=True)  # AAAA-MM

    def __repr__(self): return f"<Lanc {self.id} {self.competencia} {self.tipo} {self.valor}>"
