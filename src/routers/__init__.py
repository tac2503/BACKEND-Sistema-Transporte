from src.routers.Administradores import router as administradores_router
from src.routers.Tarjeta import router as tarjeta_router
from src.routers.Tipo_Empleado import router as tipo_empleado_router
from src.routers.Vehiculos import router as vehiculos_router

__all__=[
    "administradores_router",
    "tarjeta_router",
    "tipo_empleado_router",
    "vehiculos_router"
]