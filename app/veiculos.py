from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import db
from .models import Veiculo

bp = Blueprint("veiculos", __name__)

@bp.route("/")
@login_required
def index():
    q = request.args.get("q","").strip()
    query = Veiculo.query
    if q:
        like = f"%{q}%"
        query = query.filter((Veiculo.placa.ilike(like)) | (Veiculo.modelo.ilike(like)))
    veiculos = query.order_by(Veiculo.placa.asc()).all()
    return render_template("veiculos_list.html", veiculos=veiculos, q=q)

@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method == "POST":
        v = Veiculo(
            placa=request.form.get("placa"),
            modelo=request.form.get("modelo"),
            marca=request.form.get("marca"),
            ano=request.form.get("ano"),
            renavam=request.form.get("renavam"),
            chassi=request.form.get("chassi"),
            proprietario=request.form.get("proprietario"),
            observacoes=request.form.get("observacoes"),
        )
        db.session.add(v); db.session.commit()
        flash("Veículo criado!", "success")
        return redirect(url_for("veiculos.index"))
    return render_template("veiculos_form.html", veiculo=None)

@bp.route("/<int:vid>/editar", methods=["GET","POST"])
@login_required
def editar(vid):
    v = Veiculo.query.get_or_404(vid)
    if request.method == "POST":
        for f in ["placa","modelo","marca","ano","renavam","chassi","proprietario","observacoes"]:
            setattr(v, f, request.form.get(f))
        db.session.commit()
        flash("Veículo atualizado!", "success")
        return redirect(url_for("veiculos.index"))
    return render_template("veiculos_form.html", veiculo=v)

@bp.route("/<int:vid>/excluir", methods=["POST"])
@login_required
def excluir(vid):
    v = Veiculo.query.get_or_404(vid)
    db.session.delete(v); db.session.commit()
    flash("Veículo excluído.", "warning")
    return redirect(url_for("veiculos.index"))
