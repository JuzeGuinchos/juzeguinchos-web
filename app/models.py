from datetime import datetime
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(32), index=True)
    razao_social = db.Column(db.String(255))
    nome_fantasia = db.Column(db.String(255))
    cep = db.Column(db.String(32))
    logradouro = db.Column(db.String(255))
    numero = db.Column(db.String(64))
    complemento = db.Column(db.String(255))
    bairro = db.Column(db.String(255))
    municipio = db.Column(db.String(255))
    uf = db.Column(db.String(8))
    telefone = db.Column(db.String(64))
    email = db.Column(db.String(255))
    inscricao_estadual = db.Column(db.String(64))
    observacoes = db.Column(db.Text)

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(32), index=True)
    modelo = db.Column(db.String(128))
    marca = db.Column(db.String(128))
    ano = db.Column(db.String(16))
    renavam = db.Column(db.String(64))
    chassi = db.Column(db.String(64))
    proprietario = db.Column(db.String(128))
    observacoes = db.Column(db.Text)

class Lancamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=datetime.utcnow)
    tipo = db.Column(db.String(32))
    cliente = db.Column(db.String(255))
    cnpj = db.Column(db.String(32))
    veiculo = db.Column(db.String(255))
    placa = db.Column(db.String(32))
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(128))
    valor = db.Column(db.Numeric(14,2))
    origem = db.Column(db.String(255))
    destino = db.Column(db.String(255))
    cidade_despesa = db.Column(db.String(255))
