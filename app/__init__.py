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

        from .views import (
            UsuarioView, TecnicoView, CategoriaView,
            PrioridadView, TicketView, ComentarioView
        )

        appbuilder.add_view(UsuarioView, "Usuarios", category="Gestión")
        appbuilder.add_view(TecnicoView, "Técnicos", category="Gestión")
        appbuilder.add_view(CategoriaView, "Categorías", category="Gestión")
        appbuilder.add_view(PrioridadView, "Prioridades", category="Gestión")
        appbuilder.add_view(TicketView, "Tickets", category="Gestión")
        appbuilder.add_view(ComentarioView, "Comentarios", category="Gestión")

    return app