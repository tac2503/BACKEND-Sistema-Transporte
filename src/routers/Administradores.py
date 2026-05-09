from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.schemas import AdministradorResponse, AdministradorCreate
from src.core.security import get_current_admin
from src.core.audit import registrar_auditoria
from src.core.utils import hash_password
from src.database.config import get_db
from src.models import Administrador
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(prefix="/administradores", tags=["administradores"])


@router.post(
    "/", response_model=AdministradorResponse, status_code=status.HTTP_201_CREATED
)
def create_administrador(
    administrador: AdministradorCreate, db: Session = Depends(get_db)
):
    """Crea un nuevo administrador en la base de datos."""

    exists = (
        db.query(Administrador)
        .filter(Administrador.documento == administrador.documento)
        .first()
    )
    if exists:
        raise ConflictError(message="El documento ya está registrado.")
    nuevo_administrador = Administrador(
        documento=administrador.documento,
        contrasena=hash_password(administrador.contrasena),
        nombre=administrador.nombre,
        email=administrador.email,
        telefono=administrador.telefono,
        direccion=administrador.direccion,
        descripcion=administrador.descripcion,
    )
    db.add(nuevo_administrador)
    db.commit()
    db.refresh(nuevo_administrador)
    registrar_auditoria(db, "administradores", "crear")
    return nuevo_administrador


@router.get(
    "/", response_model=list[AdministradorResponse], status_code=status.HTTP_200_OK
)
def get_administradores(
    db: Session = Depends(get_db),
    _: Administrador = Depends(get_current_admin),
):
    """Obtiene todos los administradores de la base de datos."""
    administradores = db.query(Administrador).all()
    registrar_auditoria(db, "administradores", "obtener")
    return administradores


@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_administrador(
    documento: str,
    db: Session = Depends(get_db),
    _: Administrador = Depends(get_current_admin),
):
    """Elimina un administrador de la base de datos por su documento."""
    administrador = (
        db.query(Administrador).filter(Administrador.documento == documento).first()
    )
    if not administrador:
        raise NotFoundError(message="El administrador no fue encontrado.")
    db.delete(administrador)
    db.commit()
    registrar_auditoria(db, "administradores", "eliminar")
    return {"detail": "El administrador fue eliminado."}
