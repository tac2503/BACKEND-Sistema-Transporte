from src.crud.cliente import _get, _post, _delete

def crear_tarjeta(documento_cliente: str):
    payload = {
        "documento_cliente": documento_cliente
    }
    return _post("/tarjetas/", json=payload)

def obtener_tarjetas():
    return _get("/tarjetas/")

def obtener_tarjeta(numero_tarjeta: str):
    return _get(f"/tarjetas/{numero_tarjeta}")

def eliminar_tarjeta(numero_tarjeta: str):
    return _delete(f"/tarjetas/{numero_tarjeta}")

def obtener_tarjeta(numero_tarjeta: str):
    return _get(f"/tarjetas/{numero_tarjeta}")

def eliminar_tarjeta(numero_tarjeta: str):
    return _delete(f"/tarjetas/{numero_tarjeta}")