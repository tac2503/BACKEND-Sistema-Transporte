from pydantic import BaseModel, EmailStr, Field

class ClienteCreate(BaseModel):
    documento: str = Field(..., example="12345678")
    nombre: str = Field(..., example="Juan Perez")
    email: EmailStr = Field(..., example="hola@gmail.com")
    telefono: str = Field(..., example="1234567890")
    direccion: str = Field(..., example="Calle Falsa 123")

class ClienteResponse(BaseModel):
    
    documento: str
    nombre: str
    email: EmailStr
    telefono: str
    direccion: str

    class Config:
        from_attributes = True