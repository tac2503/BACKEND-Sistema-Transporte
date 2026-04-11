from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError

from src.database.config import SessionLocal
from src.models.Aministradores import Administrador
from src.models.Empleado import Empleado
from src.models.Tipo_Empleado import Tipo_Empleado
from src.models.Rutas import Ruta
from src.models.Vehiculos import Vehiculo
from src.models.Cliente import Cliente
from src.core.utils import hash_password

load_dotenv()


ADMINISTRADOR = [
    {
        "documento": "1021923966",
        "contrasena": "Admin123!",
        "nombre": "Tomas Alvarez",
        "email": "tomasac@gmail.com",
        "telefono": "3135819710",
        "direccion": "Calle 103c#72-17",
    }
]

CLIENTE = [
    {
        "documento": "12345678",
        "contrasena": "cliente_seguro123",
        "nombre": "Juan Perez",
        "email": "juanperez@gmail.com",
        "telefono": "3123456789",
        "direccion": "Carrera 12#34-56",
    }
]

EMPLEADOS = [
    {
        "documento": "70105331",
        "nombre": "Gustavo Alvarez",
        "email": "gustavoalvarez@gmail.com",
        "telefono": "3127810335",
        "direccion": "Urbanizacion Alejandria",
        "tipo_empleado": 1,
    },
]

TIPO_EMPLEADO = [
    {"id": 1, "nombre": "Conductor"},
    {"id": 2, "nombre": "Mecanico"},
]

RUTA = [
    {
        "nombre": "Ruta 1",
        "descripcion": "Ruta que va desde la Calle 100 hasta el centro de la ciudad",
    },
    {
        "nombre": "Ruta 2",
        "descripcion": "Ruta que va desde la Iglesia San Judas hasta la UDEA",
    },
]


def obtener_ruta_id(db):
    ruta = db.query(Ruta.id).order_by(Ruta.id).first()
    return ruta[0] if ruta else None


VEHICULO = [{"placa": "BLO982", "marca": "Audi"}]


def get_or_create_admin(db):
    admin_data = ADMINISTRADOR[0]
    admin = (
        db.query(Administrador)
        .filter(Administrador.documento == admin_data["documento"])
        .first()
    )
    if admin:
        return admin
    u = admin_data.copy()
    u["contrasena"] = hash_password(u["contrasena"])
    admin = Administrador(**u)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Administrador creado: {admin.documento}")
    return admin


def seed_tipos_empleado(db):
    for tipo in TIPO_EMPLEADO:
        if db.query(Tipo_Empleado).filter(Tipo_Empleado.id == tipo["id"]).first():
            continue
        db.add(Tipo_Empleado(id=tipo["id"], nombre_Tipo=tipo["nombre"]))
        print(f"Tipo de empleado creado: {tipo['nombre']}")
    db.commit()


def seed_clientes(db):
    for cliente in CLIENTE:
        if db.query(Cliente).filter(Cliente.documento == cliente["documento"]).first():
            continue
        u = cliente.copy()
        u["contrasena"] = hash_password(u["contrasena"])
        db.add(Cliente(**u))
        print(f"Cliente creado: {cliente['documento']}")
    db.commit()


def seed_empleados(db):
    for empleado in EMPLEADOS:
        if (
            db.query(Empleado)
            .filter(Empleado.documento == empleado["documento"])
            .first()
        ):
            continue
        db.add(
            Empleado(
                documento=empleado["documento"],
                nombre=empleado["nombre"],
                email=empleado["email"],
                telefono=empleado["telefono"],
                direccion=empleado["direccion"],
                Tipo_Empleado_id=empleado["tipo_empleado"],
            )
        )
        print(f"Empleado creado: {empleado['documento']}")
    db.commit()


def seed_rutas(db):
    for ruta in RUTA:
        if db.query(Ruta).filter(Ruta.nombre == ruta["nombre"]).first():
            continue
        db.add(Ruta(nombre=ruta["nombre"], descripcion=ruta["descripcion"]))
        print(f"Ruta creada: {ruta['nombre']}")
    db.commit()


def seed_vehiculos(db):
    ruta_id = obtener_ruta_id(db)
    if not ruta_id:
        raise RuntimeError("No existe ninguna ruta para asociar el vehículo.")
    for vehiculo in VEHICULO:
        if db.query(Vehiculo).filter(Vehiculo.placa == vehiculo["placa"]).first():
            continue
        db.add(
            Vehiculo(
                placa=vehiculo["placa"],
                marca=vehiculo["marca"],
                ruta_id=ruta_id,
            )
        )
        print(f"Vehículo creado: {vehiculo['placa']}")
    db.commit()


def main():
    try:
        db = SessionLocal()
        try:
            print("Sembrando admin si no existe...")
            get_or_create_admin(db)
            print("Sembrando tipos de empleado...")
            seed_tipos_empleado(db)
            print("Sembrando empleados...")
            seed_empleados(db)
            print("Sembrando clientes...")
            seed_clientes(db)
            print("Sembrando rutas...")
            seed_rutas(db)
            print("Sembrando vehículos...")
            seed_vehiculos(db)
        finally:
            db.close()
    except OperationalError as e:
        print(
            "Error de conexión a la base de datos. Asegúrate de que el servidor de la base de datos esté en funcionamiento y que las credenciales sean correctas."
        )
        print(f"Detalles del error: {e}")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
