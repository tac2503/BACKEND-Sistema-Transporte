from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.database.config import Base

class Tipo_Empleado(Base):
    __tablename__ = "tipos_empleados"

    id = Column(Integer, primary_key=True,  index=True, autoincrement=True)
    nombre_Tipo = Column(String, nullable=False)

    
    