from pydantic import BaseModel, Field


class Tipo_EmpleadoCreate(BaseModel):
    """Esquema de entrada para crear tipos de empleado."""

    nombre_Tipo: str = Field(..., example="Conductor")


class Tipo_EmpleadoResponse(BaseModel):
    """Esquema de salida para tipos de empleado."""

    id: int
    nombre_Tipo: str

    class Config:
        from_attributes = True
