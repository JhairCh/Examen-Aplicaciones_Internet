from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Usuario(Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    telefono = Column(String(20))
    tickets = relationship("Ticket", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")

    def __repr__(self):
        return self.nombre



class Tecnico(Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(120), unique=True, nullable=False)
    especialidad = Column(String(100))
    tickets = relationship("Ticket", back_populates="tecnico")

    def __repr__(self):
        return self.nombre


class Categoria(Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), unique=True, nullable=False)
    descripcion = Column(Text)
    tickets = relationship("Ticket", back_populates="categoria")

    def __repr__(self):
        return self.nombre


class Prioridad(Model):
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    nivel = Column(Integer, nullable=False)
    tickets = relationship("Ticket", back_populates="prioridad")

    def __repr__(self):
        return self.nombre


class Ticket(Model):
    id = Column(Integer, primary_key=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String(30), default="Pendiente", nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())

    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("tecnico.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    prioridad_id = Column(Integer, ForeignKey("prioridad.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="tickets")
    tecnico = relationship("Tecnico", back_populates="tickets")
    categoria = relationship("Categoria", back_populates="tickets")
    prioridad = relationship("Prioridad", back_populates="tickets")
    comentarios = relationship(
        "Comentario",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return self.titulo



class Comentario(Model):
    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())

    ticket_id = Column(Integer, ForeignKey("ticket.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    ticket = relationship("Ticket", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")

    def __repr__(self):
        return f"Comentario {self.id}"


