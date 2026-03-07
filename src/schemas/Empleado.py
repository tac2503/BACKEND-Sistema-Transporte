from pydantic import BaseModel, EmailStr, Field

class EmpleadoCreate(BaseModel):
    documento: str = Field(..., example="12345678")
    nombre: str = Field(..., example="Juan Perez")
    email: EmailStr = Field(..., example="hola@gmail.com")
    telefono: str = Field(..., example="1234567890")
    direccion: str = Field(..., example="Calle Falsa 123")
    Tipo_Empleado_id: int = Field(..., example=1)