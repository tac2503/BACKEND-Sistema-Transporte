import httpx

BASE_URL = "http://localhost:8000"


def _get(url: str, **kwargs) -> dict | list:
    """Ejecuta una peticion GET y retorna el JSON de respuesta."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.get(url, **kwargs)
        r.raise_for_status()
        return r.json()


def _post(url: str, json: dict, **kwargs) -> dict:
    """Ejecuta una peticion POST y retorna el cuerpo JSON."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.post(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _put(url: str, json: dict, **kwargs) -> dict:
    """Ejecuta una peticion PUT y retorna el JSON resultante."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.put(url, json=json, **kwargs)
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _delete(url: str, **kwargs) -> None:
    """Ejecuta una peticion DELETE y valida el estado HTTP."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.delete(url, **kwargs)
        r.raise_for_status()