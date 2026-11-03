from flask import Flask, request, jsonify
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

        @app.route("/api/analizar-ticket", methods=["POST"])
        def api_analizar_ticket():
            from .ai_service import analizar_ticket

            datos = request.get_json(silent=True) or {}

            titulo = datos.get("titulo", "").strip()
            descripcion = datos.get("descripcion", "").strip()

            if not titulo or not descripcion:
                return jsonify({
                    "error": "El título y la descripción son obligatorios."
                }), 400

            categorias = [
                c.nombre for c in models.Categoria.query.all()
            ]

            prioridades = [
                p.nombre for p in models.Prioridad.query.all()
            ]

            resultado = analizar_ticket(
                titulo,
                descripcion,
                categorias,
                prioridades
            )

            if "error" in resultado:
                return jsonify(resultado), 500

            return jsonify(resultado)

    return app