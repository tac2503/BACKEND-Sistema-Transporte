from fastapi import APIRouter, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.audit import registrar_auditoria
from src.core.exceptions import ConflictError, NotFoundError
from src.core.security import get_current_admin
from src.database.config import get_db
from src.models import Ruta, Vehiculo
from src.schemas import RutaCreate, RutaPublicResponse, RutaResponse

router = APIRouter(prefix="/rutas", tags=["rutas"])


@router.post("/", response_model=RutaResponse, status_code=status.HTTP_201_CREATED)
def crear_ruta(
    ruta: RutaCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
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
    return nueva_ruta


@router.get("/", response_model=list[RutaResponse], status_code=status.HTTP_200_OK)
def get_rutas(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    """Lista todas las rutas registradas."""
    rutas = db.query(Ruta).all()
    return rutas


@router.get(
    "/public", response_model=list[RutaPublicResponse], status_code=status.HTTP_200_OK
)
def get_rutas_public(db: Session = Depends(get_db)):
    """Lista todas las rutas registradas para clientes autenticados o visitantes."""
    rutas = db.query(Ruta).all()
    vehiculos = db.query(Vehiculo).all()
    vehiculo_por_ruta = {}
    for vehiculo in vehiculos:
        vehiculo_por_ruta.setdefault(vehiculo.ruta_id, vehiculo)
    registrar_auditoria(db, "rutas", "obtener")
    return [
        {
            "id": ruta.id,
            "nombre": ruta.nombre,
            "descripcion": ruta.descripcion,
            "vehiculo_placa": (
                vehiculo_por_ruta[ruta.id].placa
                if ruta.id in vehiculo_por_ruta
                else None
            ),
            "vehiculo_marca": (
                vehiculo_por_ruta[ruta.id].marca
                if ruta.id in vehiculo_por_ruta
                else None
            ),
        }
        for ruta in rutas
    ]


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ruta(
    id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """Elimina una ruta por su identificador."""
    ruta = db.query(Ruta).filter(Ruta.id == id).first()
    if not ruta:
        raise NotFoundError(message="La ruta no fue encontrada.")
    db.delete(ruta)
    db.commit()
    return {"detail": "La ruta fue eliminada."}
