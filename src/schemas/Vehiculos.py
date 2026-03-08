from pydantic import BaseModel, EmailStr, Field

class VehiculoCreate(BaseModel):
    placa: str = Field(..., example="ABC123")
    marca: str = Field(..., example="Mercedez-Benz")
    email: EmailStr = Field(..., example="hola@gmail.com")
    ruta_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    