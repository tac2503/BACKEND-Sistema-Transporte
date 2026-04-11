from src.routers.Auth import router as auth_router
from src.routers.Administradores import router as administradores_router
from src.routers.Cliente import router as cliente_router
from src.routers.Empleado import router as empleado_router
from src.routers.Tarjeta import router as tarjeta_router
from src.routers.Tipo_Empleado import router as tipo_empleado_router
from src.routers.Vehiculos import router as vehiculos_router
from src.routers.Rutas import router as rutas_router

__all__ = [
    "administradores_router",
    "auth_router",
    "cliente_router",
    "empleado_router",
    "tarjeta_router",
    "tipo_empleado_router",
    "vehiculos_router",
    "rutas_router",
]
