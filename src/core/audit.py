from sqlalchemy.orm import Session

from src.models import Auditoria


def registrar_auditoria(db: Session, tabla: str, accion: str) -> None:
    """Guarda un evento de auditoria en la base de datos."""

    db.add(Auditoria(tabla=tabla, accion=accion))
    db.commit()
