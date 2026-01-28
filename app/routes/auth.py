"""Login and logout (session-based)."""
from flask import Blueprint, redirect, render_template, request, session, url_for
from app.models.store import verify_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("username"):
            return redirect(url_for("dashboard.dashboard"))
        return render_template("login.html")
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    if not username or not password:
        return render_template("login.html", error="Username and password required."), 400
    if not verify_user(username, password):
        return render_template("login.html", error="Invalid username or password."), 401
    session["username"] = username
    return redirect(url_for("dashboard.dashboard"))


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("public.index"))
