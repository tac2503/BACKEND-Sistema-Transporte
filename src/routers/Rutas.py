from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin, get_current_token_payload
from src.core.audit import registrar_auditoria
from src.schemas import RutaResponse, RutaCreate
from src.database.config import get_db
from src.models import Ruta
from sqlalchemy import func
from src.core.exceptions import NotFoundError, ConflictError

router = APIRouter(prefix="/rutas", tags=["rutas"])


# Endpoints para administradores
admin_router = APIRouter(dependencies=[Depends(get_current_admin)])

@admin_router.post("/", response_model=RutaResponse, status_code=status.HTTP_201_CREATED)
def crear_ruta(ruta: RutaCreate, db: Session = Depends(get_db)):
    """Registra una ruta nueva validando que el nombre no exista."""
    exists = db.query(Ruta).filter(func.lower(Ruta.nombre) == ruta.nombre.lower()).first()
    if exists:
        raise ConflictError(
            message="La ruta con ese nombre ya está registrada.",
            details={"nombre": ruta.nombre},
        )

    nueva_ruta = Ruta(nombre=ruta.nombre, descripcion=ruta.descripcion)
    db.add(nueva_ruta)
    db.commit()
    db.refresh(nueva_ruta)
    registrar_auditoria(db, "rutas", "crear")
    return nueva_ruta

@admin_router.get("/", response_model=list[RutaResponse], status_code=status.HTTP_200_OK)
def get_rutas(db: Session = Depends(get_db)):
    """Obtiene todas las rutas registradas."""
    rutas = db.query(Ruta).all()
    registrar_auditoria(db, "rutas", "obtener")
    return rutas

@admin_router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ruta(id: int, db: Session = Depends(get_db)):
    """Elimina una ruta por su ID."""
    ruta = db.query(Ruta).filter(Ruta.id == id).first()
    if not ruta:
        raise NotFoundError(message="La ruta no fue encontrada.", details={"id": id})

    db.delete(ruta)
    db.commit()
    registrar_auditoria(db, "rutas", "eliminar")
    return {"detail": "La ruta fue eliminada."}

# Endpoint público para ver rutas
@router.get("/public", response_model=list[RutaResponse], status_code=status.HTTP_200_OK)
def get_rutas_public(db: Session = Depends(get_db)):
    """Lista todas las rutas registradas (público)."""
    rutas = db.query(Ruta).all()
    return rutas

# Incluir routers
router.include_router(admin_router)
