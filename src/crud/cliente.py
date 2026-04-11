import httpx

BASE_URL = "http://localhost:8000"
AUTH_HEADERS: dict[str, str] = {}


def set_auth_token(token: str | None) -> None:
    """Configura el token JWT que se enviará en las peticiones siguientes."""
    global AUTH_HEADERS
    AUTH_HEADERS = {"Authorization": f"Bearer {token}"} if token else {}


def _merge_headers(kwargs: dict) -> dict:
    headers = dict(AUTH_HEADERS)
    extra_headers = kwargs.pop("headers", None)
    if extra_headers:
        headers.update(extra_headers)
    if headers:
        kwargs["headers"] = headers
    return kwargs


def _get(url: str, **kwargs) -> dict | list:
    """Ejecuta una peticion GET y retorna el JSON de respuesta."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.get(url, **_merge_headers(kwargs))
        r.raise_for_status()
        return r.json()


def _post(url: str, json: dict, **kwargs) -> dict:
    """Ejecuta una peticion POST y retorna el cuerpo JSON."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.post(url, json=json, **_merge_headers(kwargs))
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _put(url: str, json: dict, **kwargs) -> dict:
    """Ejecuta una peticion PUT y retorna el JSON resultante."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.put(url, json=json, **_merge_headers(kwargs))
        r.raise_for_status()
        if r.status_code == 204:
            return {}
        return r.json()


def _delete(url: str, **kwargs) -> None:
    """Ejecuta una peticion DELETE y valida el estado HTTP."""
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as client:
        r = client.delete(url, **_merge_headers(kwargs))
        r.raise_for_status()


def login_admin(documento: str, contrasena: str) -> dict:
    """Autentica un administrador contra /auth/login/admin."""
    payload = {"documento": documento, "contrasena": contrasena}
    return _post("/auth/login/admin", json=payload)


def login_cliente(documento: str, contrasena: str) -> dict:
    """Autentica un cliente contra /auth/login/cliente."""
    payload = {"documento": documento, "contrasena": contrasena}
    return _post("/auth/login/cliente", json=payload)
