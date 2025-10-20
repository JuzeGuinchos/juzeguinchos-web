from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import func
from . import db
from .models import Cliente, Veiculo, Lancamento

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    return redirect(url_for("auth.login"))

@bp.get("/dashboard")
@login_required
def dashboard():
    total_rec = db.session.query(func.coalesce(func.sum(Lancamento.valor), 0)).filter(Lancamento.tipo=="Receita").scalar()
    total_des = db.session.query(func.coalesce(func.sum(Lancamento.valor), 0)).filter(Lancamento.tipo=="Despesa").scalar()
    liquido = (total_rec or 0) - (total_des or 0)
    ultimos = Lancamento.query.order_by(Lancamento.id.desc()).limit(10).all()
    return render_template("dashboard.html", total_rec=total_rec, total_des=total_des, liquido=liquido, ultimos=ultimos)

@bp.get("/clientes")
@login_required
def clientes_list():
    q = request.args.get("q", "").strip()
    query = Cliente.query
    if q:
        query = query.filter((Cliente.razao_social.ilike(f"%{q}%")) | (Cliente.nome_fantasia.ilike(f"%{q}%")) | (Cliente.cnpj.ilike(f"%{q}%")))
    items = query.order_by(Cliente.razao_social.asc()).limit(500).all()
    return render_template("clientes.html", items=items, q=q)

@bp.post("/clientes")
@login_required
def clientes_create():
    data = request.form.to_dict()
    c = Cliente(**data)
    db.session.add(c)
    db.session.commit()
    flash("Cliente criado.", "success")
    return redirect(url_for("main.clientes_list"))

@bp.get("/veiculos")
@login_required
def veiculos_list():
    q = request.args.get("q", "").strip()
    query = Veiculo.query
    if q:
        query = query.filter((Veiculo.placa.ilike(f"%{q}%")) | (Veiculo.modelo.ilike(f"%{q}%")) | (Veiculo.marca.ilike(f"%{q}%")))
    items = query.order_by(Veiculo.placa.asc()).limit(500).all()
    return render_template("veiculos.html", items=items, q=q)

@bp.post("/veiculos")
@login_required
def veiculos_create():
    data = request.form.to_dict()
    v = Veiculo(**data)
    db.session.add(v)
    db.session.commit()
    flash("Veículo criado.", "success")
    return redirect(url_for("main.veiculos_list"))

@bp.get("/lancamentos")
@login_required
def lanc_list():
    q = request.args.get("q", "").strip()
    query = Lancamento.query
    if q:
        query = query.filter(Lancamento.descricao.ilike(f"%{q}%"))
    items = query.order_by(Lancamento.data.desc(), Lancamento.id.desc()).limit(500).all()
    return render_template("lancamentos.html", items=items, q=q)

@bp.post("/lancamentos")
@login_required
def lanc_create():
    data = request.form.to_dict()
    if "valor" in data and data["valor"]:
        try:
            data["valor"] = float(str(data["valor"]).replace(",", ".").strip())
        except Exception:
            data["valor"] = 0.0
    from datetime import datetime
    if "data" in data and data["data"]:
        try:
            data["data"] = datetime.fromisoformat(data["data"]).date()
        except Exception:
            pass
    l = Lancamento(**data)
    db.session.add(l)
    db.session.commit()
    flash("Lançamento criado.", "success")
    return redirect(url_for("main.lanc_list"))
