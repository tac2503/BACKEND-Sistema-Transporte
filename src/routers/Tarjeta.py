from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import TarjetaResponse, TarjetaCreate
from src.database.config import get_db
from src.models import Tarjeta

router = APIRouter(
    prefix="/tarjetas",
    tags=["tarjetas"])

@router.post(
    "/", response_model=TarjetaResponse, status_code=status.HTTP_201_CREATED
)
def create_tarjeta(tarjeta: TarjetaCreate, db: Session = Depends(get_db)):
    
    # Verificar si el cliente ya tiene una tarjeta
    exists = db.query(Tarjeta).filter(Tarjeta.documento_cliente == tarjeta.documento_cliente).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El cliente ya tiene una tarjeta registrada.")
    
    nueva_tarjeta = Tarjeta(
        documento_cliente=tarjeta.documento_cliente,
        saldo=0
    )
    db.add(nueva_tarjeta)
    db.commit()
    db.refresh(nueva_tarjeta)
    return nueva_tarjeta

@router.get(
    "/", response_model=list[TarjetaResponse], status_code=status.HTTP_200_OK
)
def get_tarjetas(db: Session = Depends(get_db)):
    tarjetas = db.query(Tarjeta).all()
    return tarjetas

@router.get(
    "/{numero_tarjeta}", response_model=TarjetaResponse, status_code=status.HTTP_200_OK
)
def get_tarjeta(numero_tarjeta: str, db: Session = Depends(get_db)):
    tarjeta = db.query(Tarjeta).filter(Tarjeta.numero_tarjeta == numero_tarjeta).first()
    if not tarjeta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tarjeta no fue encontrada.")
    return tarjeta

@router.delete("/{numero_tarjeta}", status_code=status.HTTP_200_OK)
def delete_tarjeta(numero_tarjeta: str, db: Session = Depends(get_db)):
    tarjeta = db.query(Tarjeta).filter(Tarjeta.numero_tarjeta == numero_tarjeta).first()
    if not tarjeta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La tarjeta no fue encontrada.")
    db.delete(tarjeta)
    db.commit()
    return {"detail": "La tarjeta fue eliminada."}
