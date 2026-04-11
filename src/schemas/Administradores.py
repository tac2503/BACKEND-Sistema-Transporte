from pydantic import BaseModel, EmailStr, Field


class AdministradorCreate(BaseModel):
    """Esquema de entrada para crear administradores."""

    documento: str = Field(..., example="12345678")
    contrasena: str = Field(..., example="contraseña_segura")
    nombre: str = Field(..., example="Juan Perez")
    email: EmailStr = Field(..., example="hola@gmail.com")
    telefono: str = Field(..., example="1234567890")
    direccion: str = Field(..., example="Calle Falsa 123")


class AdministradorResponse(BaseModel):
    """Esquema de salida para datos de administradores."""

    documento: str
    nombre: str
    email: EmailStr
    telefono: str
    direccion: str

    class Config:
        from_attributes = True
