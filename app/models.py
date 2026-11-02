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




    