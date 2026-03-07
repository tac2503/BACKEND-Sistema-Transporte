import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database.config import Base

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(String(36),  index=True, default=lambda: str(uuid.uuid4()))
    documento = Column(String,primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

