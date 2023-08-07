from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# from app.database import Base
from utils.database.models import APIBaseModel


class User(APIBaseModel):
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    phone_number = Column(String, nullable=True)

    todos = relationship("Todo", back_populates="owner")
