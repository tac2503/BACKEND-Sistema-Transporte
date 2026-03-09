from pydantic import BaseModel, Field

class TarjetaCreate(BaseModel):
    documento_cliente: str = Field(..., example="12345678")

class TarjetaResponse(BaseModel):
    numero_tarjeta: str
    documento_cliente: str
    saldo: int

    class Config:
        from_attributes = True