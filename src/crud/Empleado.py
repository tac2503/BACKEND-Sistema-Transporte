from src.crud.cliente import _get, _post, _delete


def crear_empleado(documento: str, nombre: str, email: str, telefono: str, direccion: str, Tipo_Empleado_id: int):
    """Crea un empleado a traves del endpoint de empleados."""
    payload = {
        "documento": documento,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "direccion": direccion,
        "Tipo_Empleado_id": Tipo_Empleado_id
    }
    return _post("/empleados/", json=payload)


def obtener_empleados():
    """Recupera todos los empleados desde la API."""
    return _get("/empleados/")


def obtener_empleado(documento: str):
    """Recupera un empleado por documento."""
    return _get(f"/empleados/{documento}")


def eliminar_empleado(documento: str):
    """Elimina un empleado por documento."""
    return _delete(f"/empleados/{documento}")