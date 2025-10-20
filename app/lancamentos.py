from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from . import db
from .models import Lancamento

bp = Blueprint("lancamentos", __name__)

def _competencia_padrao():
    now = datetime.now()
    return f"{now.year:04d}-{now.month:02d}"

@bp.route("/")
@login_required
def index():
    comp = request.args.get("comp") or _competencia_padrao()
    lancs = Lancamento.query.filter_by(competencia=comp).order_by(Lancamento.data.asc()).all()
    total = sum([(l.valor or 0) if (l.tipo or "").upper()=="ENTRADA" else -(l.valor or 0) for l in lancs])
    return render_template("lanc_list.html", lancs=lancs, comp=comp, total=total)

@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method == "POST":
        l = Lancamento(
            data = datetime.strptime(request.form.get("data"), "%Y-%m-%d").date(),
            tipo = request.form.get("tipo"),
            cliente = request.form.get("cliente"),
            cnpj = request.form.get("cnpj"),
            veiculo = request.form.get("veiculo"),
            placa = request.form.get("placa"),
            descricao = request.form.get("descricao"),
            categoria = request.form.get("categoria"),
            valor = request.form.get("valor"),
            origem = request.form.get("origem"),
            destino = request.form.get("destino"),
            cidade_despesa = request.form.get("cidade_despesa"),
            competencia = request.form.get("competencia") or _competencia_padrao(),
        )
        db.session.add(l); db.session.commit()
        flash("Lançamento criado!", "success")
        return redirect(url_for("lancamentos.index", comp=l.competencia))
    return render_template("lanc_form.html", lanc=None, comp=_competencia_padrao())

@bp.route("/<int:id>/editar", methods=["GET","POST"])
@login_required
def editar(id):
    l = Lancamento.query.get_or_404(id)
    if request.method == "POST":
        for f in ["tipo","cliente","cnpj","veiculo","placa","descricao","categoria","valor","origem","destino","cidade_despesa","competencia"]:
            setattr(l, f, request.form.get(f))
        l.data = datetime.strptime(request.form.get("data"), "%Y-%m-%d").date()
        db.session.commit()
        flash("Lançamento atualizado!", "success")
        return redirect(url_for("lancamentos.index", comp=l.competencia))
    return render_template("lanc_form.html", lanc=l, comp=l.competencia)

@bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):
    l = Lancamento.query.get_or_404(id)
    comp = l.competencia
    db.session.delete(l); db.session.commit()
    flash("Lançamento excluído.", "warning")
    return redirect(url_for("lancamentos.index", comp=comp))
