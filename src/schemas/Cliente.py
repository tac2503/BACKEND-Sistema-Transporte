from pydantic import BaseModel, EmailStr, Field


class ClienteCreate(BaseModel):
    """Esquema de entrada para crear clientes."""

    documento: str = Field(..., example="12345678")
    contrasena: str = Field(..., example="cliente_seguro123")
    nombre: str = Field(..., example="Juan Perez")
    email: EmailStr = Field(..., example="hola@gmail.com")
    telefono: str = Field(..., example="1234567890")
    direccion: str = Field(..., example="Calle Falsa 123")


class ClienteResponse(BaseModel):
    """Esquema de salida para consultar clientes."""

    documento: str
    nombre: str
    email: EmailStr
    telefono: str
    direccion: str

    class Config:
        from_attributes = True
