from pydantic import BaseModel, Field


class VehiculoCreate(BaseModel):
    """Esquema de entrada para crear vehiculos."""

    placa: str = Field(..., example="ABC123")
    marca: str = Field(..., example="Mercedes-Benz")
    ruta_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")


class VehiculoResponse(BaseModel):
    """Esquema de salida para vehiculos."""

    placa: str
    marca: str
    ruta_id: str

    class Config:
        from_attributes = True
