import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.database.config import Base

class Vehiculo(Base):
    """Modelo de vehículo que representa los vehículos registrados en el sistema.
    Cada vehículo tiene una placa única, una marca y está asociado a una ruta específica."""
    __tablename__ = "vehiculos"

    id = Column(String(36),  index=True, default=lambda: str(uuid.uuid4()))
    placa = Column(String(6), primary_key=True, index=True)
    marca = Column(String, nullable=False)
    ruta_id = Column(String(36), ForeignKey("rutas.id",ondelete="CASCADE"), nullable=False)

    ruta = relationship("Ruta", back_populates="vehiculos")

