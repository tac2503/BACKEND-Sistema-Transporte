from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from src.schemas import AdministradorResponse, AdministradorCreate
from src.database.config import get_db
from src.models import Administrador

router = APIRouter(
    prefix="/administradores",
    tags=["administradores"])

@router.post(
    "/", response_model=AdministradorResponse,status_code=status.HTTP_201_CREATED
)
def create_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db)):
    
    exists = db.query(Administrador).filter(Administrador.documento == administrador.documento).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El documento ya está registrado.")
    nuevo_administrador = Administrador(
        documento=administrador.documento,
        nombre=administrador.nombre,
        email=administrador.email,
        telefono=administrador.telefono,
        direccion=administrador.direccion
    )
    db.add(nuevo_administrador)
    db.commit()
    db.refresh(nuevo_administrador)
    return nuevo_administrador

@router.get(
    "/", response_model=list[AdministradorResponse],status_code=status.HTTP_200_OK
)
def get_administradores(db: Session = Depends(get_db)):
    administradores = db.query(Administrador).all()
    return administradores

@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_administrador(documento: str, db: Session = Depends(get_db)):
    administrador = db.query(Administrador).filter(Administrador.documento == documento).first()
    if not administrador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El administrador no fue encontrado.")
    db.delete(administrador)
    db.commit()
    return {"detail": "El administrador fue eliminado."}
