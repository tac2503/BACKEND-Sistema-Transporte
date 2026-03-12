from src.crud.cliente import _get, _post, _delete


def crear_cliente(documento: str, nombre: str, email: str, telefono: str, direccion: str) -> dict:
    payload = {
        "documento": documento,
        "nombre": nombre,
        "email": email,
        "telefono": telefono,
        "direccion": direccion
    }
    return _post("/clientes/", json=payload)


def obtener_clientes() -> list:
    return _get("/clientes/")


def obtener_cliente(documento: str) -> dict:
    return _get(f"/clientes/{documento}")


def eliminar_cliente(documento: str) -> None:
    return _delete(f"/clientes/{documento}")