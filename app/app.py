"""Flask app factory for FinTrust Bank."""
from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    from app.config import get_config
    app.config.from_object(get_config())

    from app.models.store import init_db, seed_demo
    init_db()
    seed_demo()

    from app.routes.public import public_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="")
    app.register_blueprint(dashboard_bp, url_prefix="")

    return app


app = create_app()
