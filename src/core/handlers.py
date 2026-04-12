"""
Manejadores de excepciones para la API.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from .exceptions import AppException


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Manejador para excepciones personalizadas de la aplicación.
    Devuelve una respuesta JSON estructurada.
    """
    response = JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )
    if hasattr(exc, "headers") and exc.headers:
        response.headers.update(exc.headers)
    return response
