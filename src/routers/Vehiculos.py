from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin
from src.schemas import VehiculoResponse, VehiculoCreate
from src.database.config import get_db
from src.models import Vehiculo
from src.core.exceptions import ConflictError, NotFoundError

router = APIRouter(
    prefix="/vehiculos", tags=["vehiculos"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=VehiculoResponse, status_code=status.HTTP_201_CREATED)
def create_vehiculo(vehiculo: VehiculoCreate, db: Session = Depends(get_db)):
    """Registra un vehiculo nuevo validando que la placa no exista."""

    exists = db.query(Vehiculo).filter(Vehiculo.placa == vehiculo.placa).first()
    if exists:
        raise ConflictError(
            message="El vehículo con esa placa ya está registrado.",
            details={"placa": vehiculo.placa},
        )

    nuevo_vehiculo = Vehiculo(
        placa=vehiculo.placa, marca=vehiculo.marca, ruta_id=vehiculo.ruta_id
    )
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo


@router.get("/", response_model=list[VehiculoResponse], status_code=status.HTTP_200_OK)
def get_vehiculos(db: Session = Depends(get_db)):
    """Obtiene todos los vehiculos registrados en el sistema."""
    vehiculos = db.query(Vehiculo).all()
    return vehiculos


@router.get("/{placa}", response_model=VehiculoResponse, status_code=status.HTTP_200_OK)
def get_vehiculo(placa: str, db: Session = Depends(get_db)):
    """Obtiene un vehiculo especifico por su placa."""
    vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    if not vehiculo:
        raise NotFoundError(
            message="El vehículo no fue encontrado.", details={"placa": placa}
        )
    return vehiculo


@router.delete("/{placa}", status_code=status.HTTP_200_OK)
def delete_vehiculo(placa: str, db: Session = Depends(get_db)):
    """Elimina un vehiculo existente por placa."""
    vehiculo = db.query(Vehiculo).filter(Vehiculo.placa == placa).first()
    if not vehiculo:
        raise NotFoundError(
            message="El vehículo no fue encontrado.", details={"placa": placa}
        )
    db.delete(vehiculo)
    db.commit()
    return {"detail": "El vehículo fue eliminado."}
