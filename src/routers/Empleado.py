from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin
from src.schemas import EmpleadoResponse, EmpleadoCreate
from src.database.config import get_db
from src.models import Empleado
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(
    prefix="/empleados", tags=["empleados"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=EmpleadoResponse, status_code=status.HTTP_201_CREATED)
def create_empleado(empleado: EmpleadoCreate, db: Session = Depends(get_db)):
    """Crea un empleado nuevo y valida que el documento sea unico."""

    exists = db.query(Empleado).filter(Empleado.documento == empleado.documento).first()
    if exists:
        raise ConflictError(message="El documento ya está registrado.")

    nuevo_empleado = Empleado(
        documento=empleado.documento,
        nombre=empleado.nombre,
        email=empleado.email,
        telefono=empleado.telefono,
        direccion=empleado.direccion,
        Tipo_Empleado_id=empleado.Tipo_Empleado_id,
    )
    db.add(nuevo_empleado)
    db.commit()
    db.refresh(nuevo_empleado)
    return nuevo_empleado


@router.get("/", response_model=list[EmpleadoResponse], status_code=status.HTTP_200_OK)
def get_empleados(db: Session = Depends(get_db)):
    """Retorna todos los empleados registrados."""
    empleados = db.query(Empleado).all()
    return empleados


@router.get(
    "/{documento}", response_model=EmpleadoResponse, status_code=status.HTTP_200_OK
)
def get_empleado(documento: str, db: Session = Depends(get_db)):
    """Busca un empleado por documento."""
    empleado = db.query(Empleado).filter(Empleado.documento == documento).first()
    if not empleado:
        raise NotFoundError(message="El empleado no fue encontrado.")
    return empleado


@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_empleado(documento: str, db: Session = Depends(get_db)):
    """Elimina un empleado por documento si existe."""
    empleado = db.query(Empleado).filter(Empleado.documento == documento).first()
    if not empleado:
        raise NotFoundError(message="El empleado no fue encontrado.")
    db.delete(empleado)
    db.commit()
    return {"detail": "El empleado fue eliminado."}
