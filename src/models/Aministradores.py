import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database.config import Base

class Administrador(Base):
    """
    Modelo de Administrador que representa a los administradores del sistema de transporte.
    Cada administrador tiene un documento único, nombre, email, teléfono y dirección.
    """
    __tablename__ = "administradores"

    id = Column(String(36),  index=True, default=lambda: str(uuid.uuid4()))
    documento = Column(String,primary_key=True, index=True)
    contrasena = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)

