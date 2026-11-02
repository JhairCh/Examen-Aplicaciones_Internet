from flask import Flask
from .extensions import appbuilder, db
from . import models


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")

    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, db.session)
        db.create_all()

    return app