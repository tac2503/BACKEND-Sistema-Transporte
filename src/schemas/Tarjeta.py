from pydantic import BaseModel, EmailStr, Field

class TarjetaCreate(BaseModel):
    numero: str = Field(..., example="1234567890123456")
    documento_cliente: str = Field(..., example="12345678")

