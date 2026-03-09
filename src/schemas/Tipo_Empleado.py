from pydantic import BaseModel, Field

class Tipo_EmpleadoCreate(BaseModel):
    nombre_Tipo: str = Field(..., example="Conductor")

class Tipo_EmpleadoResponse(BaseModel):
    id: int
    nombre_Tipo: str

    class Config:
        from_attributes = True