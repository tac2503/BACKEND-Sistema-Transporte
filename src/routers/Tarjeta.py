from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin, get_current_token_payload
from src.core.audit import registrar_auditoria
from src.schemas import TarjetaResponse, TarjetaCreate
from src.database.config import get_db
from src.models import Tarjeta
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(prefix="/tarjetas", tags=["tarjetas"])


# Endpoints para administradores
admin_router = APIRouter(dependencies=[Depends(get_current_admin)])

admin_router.post("/", response_model=TarjetaResponse, status_code=status.HTTP_201_CREATED)(create_tarjeta)
admin_router.get("/", response_model=list[TarjetaResponse], status_code=status.HTTP_200_OK)(get_tarjetas)
admin_router.get("/{numero_tarjeta}", response_model=TarjetaResponse, status_code=status.HTTP_200_OK)(get_tarjeta)
admin_router.delete("/{numero_tarjeta}", status_code=status.HTTP_200_OK)(delete_tarjeta)
admin_router.put("/{numero_tarjeta}", status_code=status.HTTP_200_OK)(actualizar_saldo)

# Endpoint para clientes ver sus tarjetas
@router.get("/cliente", response_model=list[TarjetaResponse], status_code=status.HTTP_200_OK)
def get_tarjetas_cliente(payload=Depends(get_current_token_payload), db: Session = Depends(get_db)):
    """Obtiene las tarjetas del cliente autenticado."""
    documento = payload["sub"]
    tarjetas = db.query(Tarjeta).filter(Tarjeta.documento_cliente == documento).all()
    return tarjetas

# Endpoint para clientes recargar saldo
@router.put("/cliente/{numero_tarjeta}/recargar", status_code=status.HTTP_200_OK)
def recargar_saldo_cliente(
    numero_tarjeta: str,
    monto: int = Body(..., embed=True),
    payload=Depends(get_current_token_payload),
    db: Session = Depends(get_db),
):
    """Recarga saldo en la tarjeta del cliente autenticado."""
    documento = payload["sub"]
    tarjeta = db.query(Tarjeta).filter(
        Tarjeta.numero_tarjeta == numero_tarjeta,
        Tarjeta.documento_cliente == documento
    ).first()
    if not tarjeta:
        raise NotFoundError(message="La tarjeta no fue encontrada o no pertenece al cliente.")
    tarjeta.saldo += monto
    db.commit()
    db.refresh(tarjeta)
    registrar_auditoria(db, "tarjetas", "recargar")
    return {"saldo": tarjeta.saldo}

# Incluir routers
router.include_router(admin_router)
