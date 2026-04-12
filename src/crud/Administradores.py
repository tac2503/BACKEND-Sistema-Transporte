from src.crud.cliente import _post


def crear_administrador(
    documento: str,
    contrasena: str,
    nombre: str,
    email: str,
    telefono: str,
    direccion: str,
    descripcion: str | None = None,
):
    """Consume el endpoint para crear un administrador."""
    payload = {
        "documento": documento,
        "contrasena": contrasena,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "descripcion": descripcion,
    }
    return _post("/administradores/", json=payload)
