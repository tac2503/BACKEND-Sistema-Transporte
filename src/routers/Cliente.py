from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import ClienteResponse, ClienteCreate
from src.database.config import get_db
from src.models import Cliente

router = APIRouter(
    prefix="/clientes",
    tags=["clientes"])

@router.post(
    "/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED
)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    
    exists = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El documento ya está registrado.")
    
    nuevo_cliente = Cliente(
        documento=cliente.documento,
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

@router.get(
    "/", response_model=list[ClienteResponse], status_code=status.HTTP_200_OK
)
def get_clientes(db: Session = Depends(get_db)):
    clientes = db.query(Cliente).all()
    return clientes

@router.get(
    "/{documento}", response_model=ClienteResponse, status_code=status.HTTP_200_OK
)
def get_cliente(documento: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.documento == documento).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no fue encontrado.")
    return cliente

@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_cliente(documento: str, db: Session = Depends(get_db)):
    cliente = db.query(Cliente).filter(Cliente.documento == documento).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El cliente no fue encontrado.")
    db.delete(cliente)
    db.commit()
    return {"detail": "El cliente fue eliminado."}