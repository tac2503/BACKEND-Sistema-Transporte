from pydantic import BaseModel, Field

class TarjetaCreate(BaseModel):
    """Esquema de entrada para crear tarjetas."""
    documento_cliente: str = Field(..., example="12345678")

class TarjetaResponse(BaseModel):
    """Esquema de salida para informacion de tarjetas."""
    numero_tarjeta: str
    documento_cliente: str
    saldo: int

    class Config:
        from_attributes = True