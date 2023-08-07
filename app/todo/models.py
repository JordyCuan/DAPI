from typing import Type

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

# from app.database import Base
from utils.database.mixins import TimestampMixin
from utils.database.models import APIBaseModel

# se pase de pydantic a sqlalchemy
# si no se realizó la operación que la haga un 'middleware'

# las clases de sqlalchemy tienen que tener sus operaciones estandar
# - estas deberán de tener conciencia de que se puede necesitar authenticación o permisos

# Clase filters que iría asignado a los ListModelMixin (y posiblemente a UpdateModelMixin)
# ? La paginación debería ir incluida en el filtro?

# ??? La *CLASE* Se inicializaría con *TODOS* los objetos/clases necesarios para los MIXINS
# En los mixins sería Type[SqlAlchemy.Model]
# ? Optional: En el __init__ definir los signatures?
# Cada mixin tendrá 2 funciones. Una que hará todo lo boilerplate y un placeholder que será escrito en la clase hija
# Tendríamos que hacer las definiciones


class Todo(APIBaseModel):
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="todos")
