from src.crud.Administradores import crear_administrador
from src.crud.Vehiculos import crear_vehiculo, obtener_vehiculos, obtener_vehiculo, eliminar_vehiculo
from src.crud.Tarjeta import crear_tarjeta, obtener_tarjetas, obtener_tarjeta, eliminar_tarjeta
from src.crud.Tipo_Empleado import crear_tipo_empleado, obtener_tipos_empleados, obtener_tipo_empleado, eliminar_tipo_empleado

__all__ = [
    "crear_administrador",
    "crear_vehiculo",
    "obtener_vehiculos", 
    "obtener_vehiculo",
    "eliminar_vehiculo",
    "crear_tarjeta",
    "obtener_tarjetas",
    "obtener_tarjeta", 
    "eliminar_tarjeta",
    "crear_tipo_empleado",
    "obtener_tipos_empleados",
    "obtener_tipo_empleado",
    "eliminar_tipo_empleado"
]