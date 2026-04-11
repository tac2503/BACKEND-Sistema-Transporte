from src.crud.cliente import _get, _post, _delete


def crear_cliente(
    documento: str,
    contrasena: str,
    nombre: str,
    email: str,
    telefono: str,
    direccion: str,
) -> dict:
    """Crea un cliente usando el endpoint `/clientes/`."""
    payload = {
        "documento": documento,
        "contrasena": contrasena,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
    }
    return _post("/clientes/", json=payload)


def obtener_clientes() -> list:
    """Obtiene la lista de clientes desde la API."""
    return _get("/clientes/")


def obtener_cliente(documento: str) -> dict:
    """Obtiene un cliente puntual por documento."""
    return _get(f"/clientes/{documento}")


def eliminar_cliente(documento: str) -> None:
    """Elimina un cliente por documento en la API."""
    return _delete(f"/clientes/{documento}")
