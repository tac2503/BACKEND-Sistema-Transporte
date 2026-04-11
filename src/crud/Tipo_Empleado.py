from src.crud.cliente import _get, _post, _delete


def crear_tipo_empleado(nombre_Tipo: str):
    """Crea un tipo de empleado en la API."""
    payload = {"nombre_Tipo": nombre_Tipo}
    return _post("/tipos-empleados/", json=payload)


def obtener_tipos_empleados():
    """Obtiene todos los tipos de empleado."""
    return _get("/tipos-empleados/")


def obtener_tipo_empleado(tipo_empleado_id: int):
    """Obtiene un tipo de empleado por ID."""
    return _get(f"/tipos-empleados/{tipo_empleado_id}")


def eliminar_tipo_empleado(tipo_empleado_id: int):
    """Elimina un tipo de empleado por ID."""
    return _delete(f"/tipos-empleados/{tipo_empleado_id}")
