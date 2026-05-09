from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.core.security import get_current_admin
from src.core.audit import registrar_auditoria
from src.core.utils import hash_password
from src.schemas import ClienteResponse, ClienteCreate
from src.database.config import get_db
from src.models import Cliente
from src.core.exceptions import ConflictError, NotFoundError

router = APIRouter(
    prefix="/clientes", tags=["clientes"], dependencies=[Depends(get_current_admin)]
)


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crea un cliente nuevo si el documento no existe en la base de datos."""

    exists = db.query(Cliente).filter(Cliente.documento == cliente.documento).first()
    if exists:
        raise ConflictError(
            message="El documento ya está registrado.",
            details={"documento": cliente.documento},
        )

    nuevo_cliente = Cliente(
        documento=cliente.documento,
        contrasena=hash_password(cliente.contrasena),
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion,
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    registrar_auditoria(db, "clientes", "crear")
    return nuevo_cliente


@router.get("/", response_model=list[ClienteResponse], status_code=status.HTTP_200_OK)
def get_clientes(db: Session = Depends(get_db)):
    """Obtiene la lista completa de clientes registrados."""
    clientes = db.query(Cliente).all()
    registrar_auditoria(db, "clientes", "obtener")
    return clientes


@router.get(
    "/{documento}", response_model=ClienteResponse, status_code=status.HTTP_200_OK
)
def get_cliente(documento: str, db: Session = Depends(get_db)):
    """Obtiene un cliente por su numero de documento."""
    cliente = db.query(Cliente).filter(Cliente.documento == documento).first()
    if not cliente:
        raise NotFoundError(
            message="El cliente no fue encontrado.", details={"documento": documento}
        )
    registrar_auditoria(db, "clientes", "obtener")
    return cliente


@router.delete("/{documento}", status_code=status.HTTP_200_OK)
def delete_cliente(documento: str, db: Session = Depends(get_db)):
    """Elimina un cliente existente identificado por documento."""
    cliente = db.query(Cliente).filter(Cliente.documento == documento).first()
    if not cliente:
        raise NotFoundError(
            message="El cliente no fue encontrado.", details={"documento": documento}
        )
    db.delete(cliente)
    db.commit()
    registrar_auditoria(db, "clientes", "eliminar")
    return {"detail": "El cliente fue eliminado."}
