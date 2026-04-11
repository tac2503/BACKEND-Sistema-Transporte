from datetime import datetime, timedelta, timezone
from typing import TypedDict

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from src.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_ALGORITHM,
    get_jwt_secret_key,
)
from src.core.utils import verify_password
from src.database.config import get_db
from src.models import Administrador, Cliente


bearer_scheme = HTTPBearer(auto_error=False)


class TokenPayload(TypedDict):
    sub: str
    role: str


def create_access_token(
    subject: str, role: str, expires_delta: timedelta | None = None
) -> str:
    """Crea un JWT firmado para el sujeto indicado."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
    }
    return jwt.encode(payload, get_jwt_secret_key(), algorithm=JWT_ALGORITHM)


def _is_bcrypt_hash(value: str) -> bool:
    return (
        value.startswith("$2a$") or value.startswith("$2b$") or value.startswith("$2y$")
    )


def authenticate_admin(
    db: Session, documento: str, contrasena: str
) -> Administrador | None:
    """Valida credenciales de administrador."""
    admin = db.query(Administrador).filter(Administrador.documento == documento).first()
    if not admin:
        return None

    # Compatibilidad: si hay contraseñas antiguas en texto plano.
    if _is_bcrypt_hash(admin.contrasena):
        if not verify_password(contrasena, admin.contrasena):
            return None
    elif admin.contrasena != contrasena:
        return None

    return admin


def authenticate_cliente(
    db: Session, documento: str, contrasena: str
) -> Cliente | None:
    """Valida credenciales de cliente."""
    cliente = db.query(Cliente).filter(Cliente.documento == documento).first()
    if not cliente:
        return None

    if _is_bcrypt_hash(cliente.contrasena):
        if not verify_password(contrasena, cliente.contrasena):
            return None
    elif cliente.contrasena != contrasena:
        return None

    return cliente


def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TokenPayload:
    """Decodifica y valida el JWT recibido en Authorization: Bearer."""
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        payload = jwt.decode(token, get_jwt_secret_key(), algorithms=[JWT_ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        if not sub or role not in {"admin", "cliente"}:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return {"sub": sub, "role": role}


def get_current_admin(
    payload: TokenPayload = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> Administrador:
    """Valida el token Bearer y retorna el administrador autenticado."""
    if payload["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador.",
        )

    admin = (
        db.query(Administrador)
        .filter(Administrador.documento == payload["sub"])
        .first()
    )
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return admin


def get_current_cliente(
    payload: TokenPayload = Depends(get_current_token_payload),
    db: Session = Depends(get_db),
) -> Cliente:
    """Retorna el cliente autenticado cuando el token corresponde a rol cliente."""
    if payload["role"] != "cliente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de cliente.",
        )

    cliente = db.query(Cliente).filter(Cliente.documento == payload["sub"]).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return cliente
