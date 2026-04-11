import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.database.config import Base


class Ruta(Base):
    """Modelo de Ruta que representa las rutas de transporte en el sistema.
    Cada ruta tiene un identificador único, un nombre y una descripción."""

    __tablename__ = "rutas"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)

    vehiculos = relationship(
        "Vehiculo", back_populates="ruta", cascade="all, delete", passive_deletes=True
    )
