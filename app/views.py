from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

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


class ComentarioView(ModelView):
    datamodel = SQLAInterface(models.Comentario)