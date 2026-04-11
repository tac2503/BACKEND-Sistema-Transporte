from pydantic import BaseModel, Field


class RutaCreate(BaseModel):
    """Esquema de entrada para crear rutas."""

    nombre: str = Field(..., example="Ruta 1")
    descripcion: str = Field(..., example="Desde A hasta B")


class RutaResponse(BaseModel):
    """Esquema de salida para rutas."""

    id: str
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True
