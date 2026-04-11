from src.crud.cliente import _get, _post, _delete


def crear_vehiculo(placa: str, marca: str, ruta_id: str):
    """Crea un vehiculo y lo asocia a una ruta."""
    payload = {"placa": placa, "marca": marca, "ruta_id": ruta_id}
    return _post("/vehiculos/", json=payload)


def obtener_vehiculos():
    """Obtiene el listado de vehiculos."""
    return _get("/vehiculos/")


def obtener_vehiculo(placa: str):
    """Obtiene un vehiculo por placa."""
    return _get(f"/vehiculos/{placa}")


def eliminar_vehiculo(placa: str):
    """Elimina un vehiculo por placa."""
    return _delete(f"/vehiculos/{placa}")
