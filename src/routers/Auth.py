from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from src.core.audit import registrar_auditoria
from src.core.security import (
    authenticate_admin,
    authenticate_cliente,
    create_access_token,
    get_current_token_payload,
)
from src.database.config import get_db
from src.schemas import LoginRequest, TokenResponse
from src.core.exceptions import UnauthorizedError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login/admin", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
def login_admin(data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica un administrador y retorna un token JWT."""
    admin = authenticate_admin(db, data.documento, data.contrasena)
    if not admin:
        raise UnauthorizedError()

    token = create_access_token(subject=admin.documento, role="admin")
    registrar_auditoria(db, "auth", "login")
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "role": "admin",
    }


@router.post(
    "/login/cliente", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
def login_cliente(data: LoginRequest, db: Session = Depends(get_db)):
    """Autentica un cliente y retorna un token JWT."""
    cliente = authenticate_cliente(db, data.documento, data.contrasena)
    if not cliente:
        raise UnauthorizedError()

    token = create_access_token(subject=cliente.documento, role="cliente")
    registrar_auditoria(db, "auth", "login")
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "role": "cliente",
    }


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """Detecta si el usuario es administrador o cliente y retorna el token adecuado."""
    admin = authenticate_admin(db, data.documento, data.contrasena)
    if admin:
        token = create_access_token(subject=admin.documento, role="admin")
        registrar_auditoria(db, "auth", "login")
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "role": "admin",
        }

    cliente = authenticate_cliente(db, data.documento, data.contrasena)
    if cliente:
        token = create_access_token(subject=cliente.documento, role="cliente")
        registrar_auditoria(db, "auth", "login")
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "role": "cliente",
        }

    raise UnauthorizedError()


@router.get("/me", status_code=status.HTTP_200_OK)
def me(payload=Depends(get_current_token_payload), db: Session = Depends(get_db)):
    """Devuelve el sujeto y rol del token actual."""
    registrar_auditoria(db, "auth", "obtener")
    return payload
