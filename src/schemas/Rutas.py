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


class RutaPublicResponse(BaseModel):
    """Esquema público de rutas con el vehículo asignado, si existe."""

    id: str
    nombre: str
    descripcion: str
    vehiculo_placa: str | None = None
    vehiculo_marca: str | None = None

    class Config:
        from_attributes = True
