from src.crud.cliente import _delete, _get, _post, _put


def crear_tarjeta(documento_cliente: str):
    """Crea una tarjeta asociada a un cliente."""
    payload = {"documento_cliente": documento_cliente}
    return _post("/tarjetas/", json=payload)


def obtener_tarjetas():
    """Obtiene todas las tarjetas registradas."""
    return _get("/tarjetas/")


def obtener_tarjeta(numero_tarjeta: str):
    """Obtiene una tarjeta por numero de tarjeta."""
    return _get(f"/tarjetas/{numero_tarjeta}")


def eliminar_tarjeta(numero_tarjeta: str):
    """Elimina una tarjeta por numero de tarjeta."""
    return _delete(f"/tarjetas/{numero_tarjeta}")


def actualizar_saldo(numero_tarjeta: str, monto: int):
    """Recarga saldo de una tarjeta enviando el monto a la API."""
    return _put(f"/tarjetas/{numero_tarjeta}", json={"monto": monto})
