from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Esquema de entrada para autenticación."""

    documento: str = Field(..., example="1021923966")
    contrasena: str = Field(..., example="Admin123!")


class TokenResponse(BaseModel):
    """Esquema de salida del token de acceso."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str