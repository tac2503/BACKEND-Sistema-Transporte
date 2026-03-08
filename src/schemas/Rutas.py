from pydantic import BaseModel, EmailStr, Field

class RutaCreate(BaseModel):
    nombre: str = Field(..., example="Ruta 1")
    descripcion: str = Field(..., example="Desde A hasta B")

