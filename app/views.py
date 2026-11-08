from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import BaseView, expose
from sqlalchemy import func
from .extensions import db
from flask import g
from .filters import FiltroTicketsPorUsuario, FiltroComentariosPorUsuario

from . import models


class UsuarioView(ModelView):
    datamodel = SQLAInterface(models.Usuario)
    label_columns = {"nombre": "Nombre", "correo": "Correo"}


class TecnicoView(ModelView):
    datamodel = SQLAInterface(models.Tecnico)


class CategoriaView(ModelView):
    datamodel = SQLAInterface(models.Categoria)


class PrioridadView(ModelView):
    datamodel = SQLAInterface(models.Prioridad)


class TicketView(ModelView):
    datamodel = SQLAInterface(models.Ticket)
    add_template = "tickets/add.html"
    base_filters = [("id", FiltroTicketsPorUsuario, None)]

    def pre_add(self, item):
        usuario_fab = getattr(g, "user", None)

        if not usuario_fab:
            return

        roles = {rol.name for rol in usuario_fab.roles}

        if "Usuario" in roles and "Admin" not in roles:
            usuario = models.Usuario.query.filter_by(
                correo=usuario_fab.email
            ).first()

            if usuario:
                item.usuario = usuario

class ComentarioView(ModelView):
    datamodel = SQLAInterface(models.Comentario)

    base_filters = [
        ("id", FiltroComentariosPorUsuario, None)
    ]

    add_form_query_rel_fields = {
        "ticket": [["id", FiltroTicketsPorUsuario, None]]
    }

    edit_form_query_rel_fields = {
        "ticket": [["id", FiltroTicketsPorUsuario, None]]
    }


class ReportesView(BaseView):

    route_base = "/reportes"

    @expose("/list/")
    def list(self):

        # Reporte 1: Tickets por categoría
        tickets_categoria = (
            db.session.query(
                models.Categoria.nombre,
                func.count(models.Ticket.id)
            )
            .outerjoin(models.Ticket)
            .group_by(models.Categoria.id, models.Categoria.nombre)
            .all()
        )

        # Reporte 2: Tickets por prioridad
        tickets_prioridad = (
            db.session.query(
                models.Prioridad.nombre,
                func.count(models.Ticket.id)
            )
            .outerjoin(models.Ticket)
            .group_by(models.Prioridad.id, models.Prioridad.nombre)
            .all()
        )

        # Reporte 3: Tickets por estado
        conteo_estados = dict(
            db.session.query(
                models.Ticket.estado,
                func.count(models.Ticket.id)
            )
            .group_by(models.Ticket.estado)
            .all()
        )

        estados = ["Pendiente", "En proceso", "Resuelto"]

        tickets_estado = sorted(
            [
                (estado, conteo_estados.get(estado, 0))
                for estado in estados
            ],
            key=lambda x: x[1],
            reverse=True
        )

        return self.render_template(
            "reportes/index.html",
            tickets_categoria=tickets_categoria,
            tickets_prioridad=tickets_prioridad,
            tickets_estado=tickets_estado
        )