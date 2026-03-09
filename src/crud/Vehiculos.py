from src.crud.cliente import _get, _post, _delete

def crear_vehiculo(placa: str, marca: str, ruta_id: str):
    payload = {
        "placa": placa,
        "marca": marca,
        "ruta_id": ruta_id
    }
    return _post("/vehiculos/", json=payload)

def obtener_vehiculos():
    return _get("/vehiculos/")

def obtener_vehiculo(placa: str):
    return _get(f"/vehiculos/{placa}")

def eliminar_vehiculo(placa: str):
    return _delete(f"/vehiculos/{placa}")