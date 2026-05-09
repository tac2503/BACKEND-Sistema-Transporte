from sqlalchemy import Column, DateTime, Integer, String, func

from src.database.config import Base


class Auditoria(Base):
    """Modelo para registrar eventos de auditoria del sistema."""

    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hora = Column(DateTime, nullable=False, server_default=func.now())
    tabla = Column(String, nullable=False)
    accion = Column(String, nullable=False)
