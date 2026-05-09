from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin
from src.core.audit import registrar_auditoria
from src.schemas import RutaResponse, RutaCreate
from src.database.config import get_db
from src.models import Ruta
from sqlalchemy import func
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(
    prefix="/rutas", tags=["rutas"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=RutaResponse, status_code=status.HTTP_201_CREATED)
def crear_ruta(ruta: RutaCreate, db: Session = Depends(get_db)):
    """Crea una ruta nueva validando el nombre sin distinguir mayusculas."""

    exists = (
        db.query(Ruta).filter(func.lower(Ruta.nombre) == ruta.nombre.lower()).first()
    )
    if exists:
        raise ConflictError(message="El nombre de la ruta ya está registrado.")

    nueva_ruta = Ruta(nombre=ruta.nombre, descripcion=ruta.descripcion)
    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)
    registrar_auditoria(db, "rutas", "crear")
    return nueva_ruta


@router.get("/", response_model=list[RutaResponse], status_code=status.HTTP_200_OK)
def get_rutas(db: Session = Depends(get_db)):
    """Lista todas las rutas registradas."""
    rutas = db.query(Ruta).all()
    registrar_auditoria(db, "rutas", "obtener")
    return rutas


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ruta(id: str, db: Session = Depends(get_db)):
    """Elimina una ruta por su identificador."""
    ruta = db.query(Ruta).filter(Ruta.id == id).first()
    if not ruta:
        raise NotFoundError(message="La ruta no fue encontrada.")
    db.delete(ruta)
    db.commit()
    registrar_auditoria(db, "rutas", "eliminar")
    return {"detail": "La ruta fue eliminada."}
