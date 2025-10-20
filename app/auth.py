from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db, login_manager

bp = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

@bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@bp.post("/first-admin")
def first_admin():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return {"ok": False, "error": "username/password required"}, 400
    if User.query.filter_by(username=username).first():
        return {"ok": False, "error": "user exists"}, 400
    u = User(username=username, password_hash=generate_password_hash(password), is_admin=True)
    db.session.add(u)
    db.session.commit()
    return {"ok": True}
