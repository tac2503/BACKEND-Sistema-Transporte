from pydantic import BaseModel, EmailStr, Field

class Tipo_EmpleadoCreate(BaseModel):
    id: int = Field(..., example=1)
    nombre_Tipo: str = Field(..., example="Conductor")
    