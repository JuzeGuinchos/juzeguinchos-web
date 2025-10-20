from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import pandas as pd
from . import db
from .models import Cliente, Veiculo, Lancamento

bp = Blueprint("importar", __name__)

@bp.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        tipo = request.form.get("tipo")
        f = request.files.get("arquivo")
        if not f or not tipo:
            flash("Selecione um tipo e um arquivo .xlsx", "warning")
            return redirect(url_for("importar.index"))
        df = pd.read_excel(f)
        imp = 0
        if tipo=="clientes":
            for _,r in df.iterrows():
                c = Cliente(
                    cnpj=str(r.get("cnpj") or "").strip(),
                    razao_social=str(r.get("razao_social") or ""),
                    nome_fantasia=str(r.get("nome_fantasia") or ""),
                    cep=str(r.get("cep") or ""),
                    logradouro=str(r.get("logradouro") or ""),
                    numero=str(r.get("numero") or ""),
                    complemento=str(r.get("complemento") or ""),
                    bairro=str(r.get("bairro") or ""),
                    municipio=str(r.get("municipio") or ""),
                    uf=str(r.get("uf") or "")[:2],
                    telefone=str(r.get("telefone") or ""),
                    email=str(r.get("email") or ""),
                    inscricao_estadual=str(r.get("inscricao_estadual") or ""),
                    observacoes=str(r.get("observacoes") or ""),
                )
                db.session.add(c); imp += 1
        elif tipo=="veiculos":
            for _,r in df.iterrows():
                v = Veiculo(
                    placa=str(r.get("placa") or "").upper(),
                    modelo=str(r.get("modelo") or ""),
                    marca=str(r.get("marca") or ""),
                    ano=str(r.get("ano") or ""),
                    renavam=str(r.get("renavam") or ""),
                    chassi=str(r.get("chassi") or ""),
                    proprietario=str(r.get("proprietario") or ""),
                    observacoes=str(r.get("observacoes") or ""),
                )
                db.session.add(v); imp += 1
        elif tipo=="lancamentos":
            for _,r in df.iterrows():
                l = Lancamento(
                    data=pd.to_datetime(r.get("data")).date(),
                    tipo=str(r.get("tipo") or ""),
                    cliente=str(r.get("cliente") or ""),
                    cnpj=str(r.get("cnpj") or ""),
                    veiculo=str(r.get("veiculo") or ""),
                    placa=str(r.get("placa") or ""),
                    descricao=str(r.get("descricao") or ""),
                    categoria=str(r.get("categoria") or ""),
                    valor=r.get("valor") or 0,
                    origem=str(r.get("origem") or ""),
                    destino=str(r.get("destino") or ""),
                    cidade_despesa=str(r.get("cidade_despesa") or ""),
                    competencia=str(r.get("competencia") or ""),
                )
                db.session.add(l); imp += 1
        else:
            flash("Tipo de importação inválido.", "danger")
            return redirect(url_for("importar.index"))

        db.session.commit()
        flash(f"Importados {imp} registros em {tipo}.", "success")
        return redirect(url_for("importar.index"))

    return render_template("importar.html")
