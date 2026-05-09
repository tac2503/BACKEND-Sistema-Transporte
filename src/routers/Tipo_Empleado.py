from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin
from src.core.audit import registrar_auditoria
from src.schemas import Tipo_EmpleadoResponse, Tipo_EmpleadoCreate
from src.database.config import get_db
from src.models import Tipo_Empleado
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(
    prefix="/tipos-empleados",
    tags=["tipos-empleados"],
    dependencies=[Depends(get_current_admin)],
)


@router.post(
    "/", response_model=Tipo_EmpleadoResponse, status_code=status.HTTP_201_CREATED
)
def create_tipo_empleado(
    tipo_empleado: Tipo_EmpleadoCreate, db: Session = Depends(get_db)
):
    """Crea un tipo de empleado nuevo si el nombre no esta registrado."""

    exists = (
        db.query(Tipo_Empleado)
        .filter(Tipo_Empleado.nombre_Tipo == tipo_empleado.nombre_Tipo)
        .first()
    )
    if exists:
        raise ConflictError(message="El tipo de empleado ya está registrado.")

    nuevo_tipo_empleado = Tipo_Empleado(nombre_Tipo=tipo_empleado.nombre_Tipo)
    db.add(nuevo_tipo_empleado)
    db.commit()
    db.refresh(nuevo_tipo_empleado)
    registrar_auditoria(db, "tipos_empleados", "crear")
    return nuevo_tipo_empleado


@router.get(
    "/", response_model=list[Tipo_EmpleadoResponse], status_code=status.HTTP_200_OK
)
def get_tipos_empleados(db: Session = Depends(get_db)):
    """Lista todos los tipos de empleado disponibles."""
    tipos_empleados = db.query(Tipo_Empleado).all()
    registrar_auditoria(db, "tipos_empleados", "obtener")
    return tipos_empleados


@router.get(
    "/{tipo_empleado_id}",
    response_model=Tipo_EmpleadoResponse,
    status_code=status.HTTP_200_OK,
)
def get_tipo_empleado(tipo_empleado_id: int, db: Session = Depends(get_db)):
    """Obtiene un tipo de empleado por su identificador."""
    tipo_empleado = (
        db.query(Tipo_Empleado).filter(Tipo_Empleado.id == tipo_empleado_id).first()
    )
    if not tipo_empleado:
        raise NotFoundError(message="El tipo de empleado no fue encontrado.")
    registrar_auditoria(db, "tipos_empleados", "obtener")
    return tipo_empleado


@router.delete("/{tipo_empleado_id}", status_code=status.HTTP_200_OK)
def delete_tipo_empleado(tipo_empleado_id: int, db: Session = Depends(get_db)):
    """Elimina un tipo de empleado por ID."""
    tipo_empleado = (
        db.query(Tipo_Empleado).filter(Tipo_Empleado.id == tipo_empleado_id).first()
    )
    if not tipo_empleado:
        raise NotFoundError(message="El tipo de empleado no fue encontrado.")
    db.delete(tipo_empleado)
    db.commit()
    registrar_auditoria(db, "tipos_empleados", "eliminar")
    return {"detail": "El tipo de empleado fue eliminado."}
