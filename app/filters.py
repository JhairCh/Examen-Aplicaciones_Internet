from flask import g
from flask_appbuilder.models.filters import BaseFilter
from . import models


class FiltroTicketsPorUsuario(BaseFilter):

    def apply(self, query, value):
        usuario_fab = getattr(g, "user", None)

        if not usuario_fab or getattr(usuario_fab, "is_anonymous", True):
            return query.filter(models.Ticket.id == -1)

        roles = {rol.name for rol in getattr(usuario_fab, "roles", [])}

        # El administrador puede ver todos los tickets
        if "Admin" in roles:
            return query

        correo = getattr(usuario_fab, "email", None)

        if not correo:
            return query.filter(models.Ticket.id == -1)

        # Usuario: solo sus propios tickets
        if "Usuario" in roles:
            usuario = models.Usuario.query.filter_by(correo=correo).first()

            if usuario:
                return query.filter(models.Ticket.usuario_id == usuario.id)

        # Técnico: solo los tickets que tiene asignados
        if "Tecnico" in roles:
            tecnico = models.Tecnico.query.filter_by(correo=correo).first()

            if tecnico:
                return query.filter(models.Ticket.tecnico_id == tecnico.id)

        # Si no existe una correspondencia, no mostrar registros
        return query.filter(models.Ticket.id == -1)


class FiltroComentariosPorUsuario(BaseFilter):

    def apply(self, query, value):
        usuario_fab = getattr(g, "user", None)

        if not usuario_fab or getattr(usuario_fab, "is_anonymous", True):
            return query.filter(models.Comentario.id == -1)

        roles = {rol.name for rol in getattr(usuario_fab, "roles", [])}

        if "Admin" in roles:
            return query

        correo = getattr(usuario_fab, "email", None)

        if not correo:
            return query.filter(models.Comentario.id == -1)

        if "Usuario" in roles:
            usuario = models.Usuario.query.filter_by(correo=correo).first()

            if usuario:
                return (
                    query.join(models.Ticket)
                    .filter(models.Ticket.usuario_id == usuario.id)
                )

        if "Tecnico" in roles:
            tecnico = models.Tecnico.query.filter_by(correo=correo).first()

            if tecnico:
                return (
                    query.join(models.Ticket)
                    .filter(models.Ticket.tecnico_id == tecnico.id)
                )

        return query.filter(models.Comentario.id == -1)