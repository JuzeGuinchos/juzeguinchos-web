from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import db, User

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/first-admin", methods=["POST", "GET"])
def first_admin():
    if User.query.first():
        return {"ok": False, "message": "Admin já criado"}, 400
    user = User(username="KLAYTON")
    user.set_password("Jose@875")
    db.session.add(user)
    db.session.commit()
    return {"ok": True}

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Usuário ou senha incorretos.", "danger")
    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
