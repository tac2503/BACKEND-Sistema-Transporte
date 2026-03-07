import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.database.config import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id = Column(String(36),  index=True, default=lambda: str(uuid.uuid4()))
    documento = Column(String,primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    telefono = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    Tipo_Empleado_id = Column(Integer, ForeignKey("tipos_empleados.id",ondelete="CASCADE"), nullable=False)

    tipo_empleado = relationship("Tipo_Empleado", back_populates="empleados")