from flask_appbuilder import ModelView, BaseView, IndexView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func
from flask import g, request

from .extensions import db
from .filters import FiltroTicketsPorUsuario, FiltroComentariosPorUsuario
from . import models


class UsuarioView(ModelView):
    datamodel = SQLAInterface(models.Usuario)

    list_columns = ["nombre", "correo", "telefono"]

    label_columns = {
        "nombre": "Nombre",
        "correo": "Correo",
        "telefono": "Teléfono"
    }


class TecnicoView(ModelView):
    datamodel = SQLAInterface(models.Tecnico)

    list_columns = ["nombre", "correo", "especialidad"]

    label_columns = {
        "nombre": "Nombre",
        "correo": "Correo",
        "especialidad": "Especialidad"
    }


class CategoriaView(ModelView):
    datamodel = SQLAInterface(models.Categoria)

    list_columns = ["nombre", "descripcion"]

    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripción"
    }


class PrioridadView(ModelView):
    datamodel = SQLAInterface(models.Prioridad)

    list_columns = ["nombre", "nivel"]

    label_columns = {
        "nombre": "Nombre",
        "nivel": "Nivel"
    }


class TicketView(ModelView):
    datamodel = SQLAInterface(models.Ticket)

    add_template = "tickets/add.html"

    base_filters = [("id", FiltroTicketsPorUsuario, None)]

    list_columns = [
        "titulo",
        "usuario",
        "tecnico",
        "categoria",
        "prioridad",
        "estado",
        "fecha_creacion"
    ]

    label_columns = {
        "titulo": "Título",
        "usuario": "Usuario",
        "tecnico": "Técnico asignado",
        "categoria": "Categoría",
        "prioridad": "Prioridad",
        "estado": "Estado",
        "fecha_creacion": "Fecha de creación"
    }

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

    def post_add(self, item):
        solucion = request.form.get("solucion_ia", "").strip()

        if solucion and item.usuario:
            comentario = models.Comentario(
                contenido=solucion,
                ticket=item,
                usuario=item.usuario
            )

            db.session.add(comentario)
            db.session.commit()

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

    list_columns = [
        "contenido",
        "ticket",
        "usuario",
        "fecha_creacion"
    ]

    label_columns = {
        "contenido": "Comentario",
        "ticket": "Ticket",
        "usuario": "Usuario",
        "fecha_creacion": "Fecha de creación"
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

class TecnoGestIndexView(IndexView):
    index_template = "index.html"