from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import EmpleadoResponse, EmpleadoCreate
from src.database.config import get_db
from src.models import Empleado

router = APIRouter(
    prefix="/empleados",
    tags=["empleados"])

@router.post(
    "/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED
)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    
    exists = db.query(Empleado).filter(Empleado.documento == empleado.documento).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El documento ya está registrado.")
    
    nuevo_empleado = Empleado(
        documento=empleado.documento,
        nombre=empleado.nombre,
        email=empleado.email,
        telefono=empleado.telefono,
        direccion=empleado.direccion,
        Tipo_Empleado_id=empleado.Tipo_Empleado_id
    )
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado

@router.get(
    "/", response_model=list[EmpleadoResponse], status_code=status.HTTP_200_OK
)
def get_empleados(db: Session = Depends(get_db)):
    empleados = db.query(Empleado).all()
    return empleados

@router.get(
    "/{documento}", response_model=EmpleadoResponse, status_code=status.HTTP_200_OK
)
def get_empleado(documento: str, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.documento == documento).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El empleado no fue encontrado.")
    return empleado

@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_empleado(documento: str, db: Session = Depends(get_db)):
    empleado = db.query(Empleado).filter(Empleado.documento == documento).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El empleado no fue encontrado.")
    db.delete(empleado)
    db.commit()
    return {"detail": "El empleado fue eliminado."}