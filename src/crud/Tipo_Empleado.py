from src.crud.cliente import _get, _post, _delete

def crear_tipo_empleado(nombre_Tipo: str):
    payload = {
        "nombre_Tipo": nombre_Tipo
    }
    return _post("/tipos-empleados/", json=payload)

def obtener_tipos_empleados():
    return _get("/tipos-empleados/")

def obtener_tipo_empleado(tipo_empleado_id: int):
    return _get(f"/tipos-empleados/{tipo_empleado_id}")

def eliminar_tipo_empleado(tipo_empleado_id: int):
    return _delete(f"/tipos-empleados/{tipo_empleado_id}")