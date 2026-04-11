from src.crud.cliente import _get, _post, _delete


def crear_ruta(nombre: str, descripcion: str):
    """Crea una ruta nueva en la API."""
    payload = {"nombre": nombre, "descripcion": descripcion}
    return _post("/rutas/", json=payload)


def obtener_rutas():
    """Obtiene todas las rutas registradas."""
    return _get("/rutas/")


def eliminar_ruta(id: str):
    """Elimina una ruta por su identificador."""
    return _delete(f"/rutas/{id}")
