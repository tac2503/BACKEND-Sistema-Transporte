from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from src.core.audit import registrar_auditoria
from src.core.exceptions import ConflictError, NotFoundError
from src.core.security import get_current_admin, get_current_cliente
from src.database.config import get_db
from src.models import Tarjeta
from src.schemas import TarjetaCreate, TarjetaResponse

router = APIRouter(prefix="/tarjetas", tags=["tarjetas"])


@router.post("/", response_model=TarjetaResponse, status_code=status.HTTP_201_CREATED)
def create_tarjeta(
    tarjeta: TarjetaCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Crea una tarjeta para un cliente que aun no tenga una asignada."""

    # Verificar si el cliente ya tiene una tarjeta
    exists = (
        db.query(Tarjeta)
        .filter(Tarjeta.documento_cliente == tarjeta.documento_cliente)
        .first()
    )
    if exists:
        raise ConflictError(message="El cliente ya tiene una tarjeta registrada.")

    nueva_tarjeta = Tarjeta(documento_cliente=tarjeta.documento_cliente, saldo=0)
    db.add(nueva_tarjeta)
    db.commit()
    db.refresh(nueva_tarjeta)
    registrar_auditoria(db, "tarjetas", "crear")
    return nueva_tarjeta


@router.get("/", response_model=list[TarjetaResponse], status_code=status.HTTP_200_OK)
def get_tarjetas(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Obtiene todas las tarjetas registradas en la base de datos."""
    tarjetas = db.query(Tarjeta).all()
    registrar_auditoria(db, "tarjetas", "obtener")
    return tarjetas


@router.get(
    "/cliente", response_model=list[TarjetaResponse], status_code=status.HTTP_200_OK
)
def get_tarjetas_cliente(
    db: Session = Depends(get_db), cliente=Depends(get_current_cliente)
):
    """Obtiene las tarjetas asociadas al cliente autenticado."""
    tarjetas = (
        db.query(Tarjeta).filter(Tarjeta.documento_cliente == cliente.documento).all()
    )
    registrar_auditoria(db, "tarjetas", "obtener")
    return tarjetas


@router.post(
    "/cliente", response_model=TarjetaResponse, status_code=status.HTTP_201_CREATED
)
def create_tarjeta_cliente(
    db: Session = Depends(get_db), cliente=Depends(get_current_cliente)
):
    """Crea una tarjeta para el cliente autenticado."""
    exists = (
        db.query(Tarjeta).filter(Tarjeta.documento_cliente == cliente.documento).first()
    )
    if exists:
        raise ConflictError(message="Ya tienes una tarjeta registrada.")

    nueva_tarjeta = Tarjeta(documento_cliente=cliente.documento, saldo=0)
    db.add(nueva_tarjeta)
    db.commit()
    db.refresh(nueva_tarjeta)
    registrar_auditoria(db, "tarjetas", "crear")
    return nueva_tarjeta


@router.get(
    "/{numero_tarjeta}", response_model=TarjetaResponse, status_code=status.HTTP_200_OK
)
def get_tarjeta(
    numero_tarjeta: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """Obtiene una tarjeta por su numero unico."""
    tarjeta = db.query(Tarjeta).filter(Tarjeta.numero_tarjeta == numero_tarjeta).first()
    if not tarjeta:
        raise NotFoundError(message="La tarjeta no fue encontrada.")
    registrar_auditoria(db, "tarjetas", "obtener")
    return tarjeta


@router.delete("/{numero_tarjeta}", status_code=status.HTTP_200_OK)
def delete_tarjeta(
    numero_tarjeta: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """Elimina una tarjeta por numero de tarjeta."""
    tarjeta = db.query(Tarjeta).filter(Tarjeta.numero_tarjeta == numero_tarjeta).first()
    if not tarjeta:
        raise NotFoundError(message="La tarjeta no fue encontrada.")
    db.delete(tarjeta)
    db.commit()
    registrar_auditoria(db, "tarjetas", "eliminar")
    return {"detail": "La tarjeta fue eliminada."}


@router.put("/{numero_tarjeta}", status_code=status.HTTP_200_OK)
def actualizar_saldo(
    numero_tarjeta: str,
    monto: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    """Incrementa el saldo de una tarjeta con el monto recibido."""
    tarjeta = db.query(Tarjeta).filter(Tarjeta.numero_tarjeta == numero_tarjeta).first()
    if not tarjeta:
        raise NotFoundError(message="La tarjeta no fue encontrada.")
    tarjeta.saldo += monto
    db.commit()
    db.refresh(tarjeta)
    registrar_auditoria(db, "tarjetas", "actualizar")
    return tarjeta.saldo


@router.put("/cliente/{numero_tarjeta}/recargar", status_code=status.HTTP_200_OK)
def recargar_saldo_cliente(
    numero_tarjeta: str,
    monto: int = Body(..., embed=True),
    db: Session = Depends(get_db),
    cliente=Depends(get_current_cliente),
):
    """Recarga la tarjeta del cliente autenticado."""
    tarjeta = (
        db.query(Tarjeta)
        .filter(
            Tarjeta.numero_tarjeta == numero_tarjeta,
            Tarjeta.documento_cliente == cliente.documento,
        )
        .first()
    )
    if not tarjeta:
        raise NotFoundError(message="La tarjeta no fue encontrada.")

    tarjeta.saldo += monto
    db.commit()
    db.refresh(tarjeta)
    registrar_auditoria(db, "tarjetas", "actualizar")
    return {"saldo": tarjeta.saldo}
