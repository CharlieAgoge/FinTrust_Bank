"""Dashboard: welcome, balance, transfer."""
from flask import Blueprint, redirect, render_template, request, session, url_for
from functools import wraps
from app.models.store import get_balance, transfer

dashboard_bp = Blueprint("dashboard", __name__)


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapped


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    username = session["username"]
    balance = get_balance(username)
    if balance is None:
        balance = 0.0
    message = None
    error = None
    if request.method == "POST":
        to_user = (request.form.get("to_user") or "").strip()
        try:
            amount = float(request.form.get("amount") or "0")
        except ValueError:
            amount = 0.0
        if to_user and amount > 0:
            ok, msg = transfer(username, to_user, amount)
            if ok:
                message = msg
                balance = get_balance(username) or 0.0
            else:
                error = msg
    return render_template(
        "dashboard.html",
        username=username,
        balance=balance,
        message=message,
        error=error,
    )
