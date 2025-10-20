from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import db
from .models import Cliente

bp = Blueprint("clientes", __name__)

@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    query = Cliente.query
    if q:
        like = f"%{q}%"
        query = query.filter((Cliente.razao_social.ilike(like)) | (Cliente.cnpj.ilike(like)))
    clientes = query.order_by(Cliente.razao_social.asc()).all()
    return render_template("clientes_list.html", clientes=clientes, q=q)

@bp.route("/novo", methods=["GET","POST"])
@login_required
def novo():
    if request.method == "POST":
        c = Cliente(
            cnpj=request.form.get("cnpj") or None,
            razao_social=request.form.get("razao_social"),
            nome_fantasia=request.form.get("nome_fantasia"),
            cep=request.form.get("cep"),
            logradouro=request.form.get("logradouro"),
            numero=request.form.get("numero"),
            complemento=request.form.get("complemento"),
            bairro=request.form.get("bairro"),
            municipio=request.form.get("municipio"),
            uf=request.form.get("uf"),
            telefone=request.form.get("telefone"),
            email=request.form.get("email"),
            inscricao_estadual=request.form.get("inscricao_estadual"),
            observacoes=request.form.get("observacoes"),
        )
        db.session.add(c); db.session.commit()
        flash("Cliente criado!", "success")
        return redirect(url_for("clientes.index"))
    return render_template("clientes_form.html", cliente=None)

@bp.route("/<int:cid>/editar", methods=["GET","POST"])
@login_required
def editar(cid):
    c = Cliente.query.get_or_404(cid)
    if request.method == "POST":
        for f in ["cnpj","razao_social","nome_fantasia","cep","logradouro","numero","complemento","bairro","municipio","uf","telefone","email","inscricao_estadual","observacoes"]:
            setattr(c, f, request.form.get(f))
        db.session.commit()
        flash("Cliente atualizado!", "success")
        return redirect(url_for("clientes.index"))
    return render_template("clientes_form.html", cliente=c)

@bp.route("/<int:cid>/excluir", methods=["POST"])
@login_required
def excluir(cid):
    c = Cliente.query.get_or_404(cid)
    db.session.delete(c); db.session.commit()
    flash("Cliente excluído.", "warning")
    return redirect(url_for("clientes.index"))
