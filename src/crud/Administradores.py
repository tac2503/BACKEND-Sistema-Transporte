from src.crud.cliente import _get, _post, _delete

def crear_administrador(documento:str,nombre:str,email:str,telefono:str,direccion:str):
    """Consume el endpoint para crear un administrador."""
    payload={
        "documento":documento,
        "nombre": nombre,
        "email":email,
        "telefono":telefono,
        "direccion":direccion
    }
    return _post("/administradores/",json=payload)