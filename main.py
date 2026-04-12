import threading
import time
from app import desplegar_uvicorn

from src.crud import (
    crear_administrador,
    crear_vehiculo,
    obtener_vehiculos,
    obtener_vehiculo,
    eliminar_vehiculo,
    crear_tarjeta,
    obtener_tarjetas,
    obtener_tarjeta,
    eliminar_tarjeta,
    crear_tipo_empleado,
    obtener_tipos_empleados,
    obtener_tipo_empleado,
    eliminar_tipo_empleado,
    crear_cliente,
    obtener_clientes,
    obtener_cliente,
    eliminar_cliente,
    crear_empleado,
    obtener_empleados,
    obtener_empleado,
    eliminar_empleado,
    crear_ruta,
    obtener_rutas,
    eliminar_ruta,
    actualizar_saldo,
)
from src.crud.cliente import login_admin, login_cliente, set_auth_token
from src.database.config import SessionLocal
from src.models import Administrador


def solicitar_login():
    """Pide credenciales al inicio y devuelve el rol autenticado."""
    while True:
        print("\nInicio de sesión")
        print("1. Administrador")
        print("2. Cliente")
        print("0. Salir")

        opcion = input("Ingrese su opción: ").strip()

        if opcion == "0":
            return None

        documento = input("Documento: ").strip()
        contrasena = input("Contraseña: ").strip()

        try:
            if opcion == "1":
                respuesta = login_admin(documento, contrasena)
            elif opcion == "2":
                respuesta = login_cliente(documento, contrasena)
            else:
                print("Opción no válida.")
                continue

            # Verificar si hay error en la respuesta
            if "error" in respuesta:
                error_info = respuesta["error"]
                print(f"Error de autenticación: {error_info['message']}")
                continue

            token = respuesta.get("access_token")
            role = respuesta.get("role")
            if not token or not role:
                print("La autenticación no devolvió la información esperada.")
                continue

            set_auth_token(token)
            print(f"Bienvenido, {role}.")
            return role
        except Exception as exc:
            print(f"No se pudo iniciar sesión: {exc}")


def menu(role: str):
    """Muestra y gestiona el menu interactivo para administradores y clientes."""
    while True:
        if role == "admin":
            print("\nMenú de administrador:")
            print("1.Crear administradores")
            print("2. Ver clientes")
            print("3. Ver empleados")
            print("4. Ver tarjetas")
            print("5. Ver tipos de empleados")
            print("6. Ver vehículos")
            print("7. Ver rutas")
            print("8. Registrar empleado")
            print("9. Crear tarjeta")
            print("10. Crear tipo de empleado")
            print("11. Crear vehículo")
            print("12. Salir")

            admin_opcion = input("Ingrese su opción: ")

            match admin_opcion:
                case "1":
                    documento = input("Documento: ")
                    contrasena = input("Contraseña: ")
                    nombre = input("Nombre: ")
                    email = input("Email: ")
                    telefono = input("Teléfono: ")
                    direccion = input("Dirección: ")
                    descripcion = input("Descripción (opcional, presione Enter para omitir): ").strip()
                    descripcion = descripcion if descripcion else None
                    
                    admin_nuevo = crear_administrador(
                        documento=documento,
                        contrasena=contrasena,
                        nombre=nombre,
                        email=email,
                        telefono=telefono,
                        direccion=direccion,
                        descripcion=descripcion,
                    )
                    print(f"Administrador creado: {admin_nuevo}")
                case "2":
                    clientes = obtener_clientes()
                    if clientes:
                        print("\n--- CLIENTES REGISTRADOS ---")
                        for cliente in clientes:
                            print(
                                f"Documento: {cliente['documento']}, Nombre: {cliente['nombre']}, Email: {cliente['email']}"
                            )
                    else:
                        print("No hay clientes registrados.")
                case "3":
                    empleados = obtener_empleados()
                    if empleados:
                        print("\n--- EMPLEADOS REGISTRADOS ---")
                        for empleado in empleados:
                            print(
                                f"Documento: {empleado['documento']}, Nombre: {empleado['nombre']}, Email: {empleado['email']}"
                            )
                    else:
                        print("No hay empleados registrados.")
                case "4":
                    tarjetas = obtener_tarjetas()
                    if tarjetas:
                        print("\n--- TARJETAS REGISTRADAS ---")
                        for tarjeta in tarjetas:
                            print(
                                f"Número: {tarjeta['numero_tarjeta']}, Cliente: {tarjeta['documento_cliente']}"
                            )
                    else:
                        print("No hay tarjetas registradas.")
                case "5":
                    tipos = obtener_tipos_empleados()
                    if tipos:
                        print("\n--- TIPOS DE EMPLEADO ---")
                        for tipo in tipos:
                            print(f"ID: {tipo['id']}, Nombre: {tipo['nombre_Tipo']}")
                    else:
                        print("No hay tipos de empleado registrados.")
                case "6":
                    vehiculos = obtener_vehiculos()
                    if vehiculos:
                        print("\n--- VEHÍCULOS REGISTRADOS ---")
                        for vehiculo in vehiculos:
                            print(
                                f"Placa: {vehiculo['placa']}, Marca: {vehiculo['marca']}, Ruta ID: {vehiculo['ruta_id']}"
                            )
                    else:
                        print("No hay vehículos registrados.")
                case "7":
                    rutas = obtener_rutas()
                    if rutas:
                        print("\n--- RUTAS REGISTRADAS ---")
                        for ruta in rutas:
                            print(
                                f"ID: {ruta['id']}, Nombre: {ruta['nombre']}, Descripción: {ruta['descripcion']}"
                            )
                    else:
                        print("No hay rutas registradas.")
                case "8":
                    documento = input("Documento del empleado: ")
                    nombre = input("Nombre del empleado: ")
                    email = input("Email del empleado: ")
                    telefono = input("Teléfono del empleado: ")
                    direccion = input("Dirección del empleado: ")
                    tipo_empleado_id = int(input("ID del tipo de empleado: "))
                    empleado_nuevo = crear_empleado(
                        documento, nombre, email, telefono, direccion, tipo_empleado_id
                    )
                    print(f"Empleado creado: {empleado_nuevo}")
                case "9":
                    documento_cliente = input("Documento del cliente: ")
                    tarjeta_nueva = crear_tarjeta(documento_cliente)
                    print(f"Tarjeta creada: {tarjeta_nueva}")
                case "10":
                    nombre_tipo = input("Nombre del tipo de empleado: ")
                    tipo_nuevo = crear_tipo_empleado(nombre_tipo)
                    print(f"Tipo de empleado creado: {tipo_nuevo}")
                case "11":
                    placa = input("Placa del vehículo: ")
                    marca = input("Marca del vehículo: ")
                    ruta_id = input("ID de la ruta: ")
                    vehiculo_nuevo = crear_vehiculo(placa, marca, ruta_id)
                    print(f"Vehículo creado: {vehiculo_nuevo}")
                case "12":
                    print("Saliendo del menú de administrador...")
                    break

        elif role == "cliente":
            print("\nMenú de cliente:")
            print("1. Ver tarjeta asociada")
            print("2. Recargar tarjeta")
            print("3. Consultar saldo")
            print("4. Ver rutas disponibles")
            print("5. Ver vehiculos disponibles")
            print("6. Salir")

            cliente_opcion = input("Ingrese su opción: ")

            match cliente_opcion:
                case "1":
                    documento = input("Documento del cliente: ")
                    cliente = obtener_cliente(documento)
                    if cliente:
                        print(f"\n--- INFORMACIÓN DEL CLIENTE ---")
                        print(f"Documento: {cliente['documento']}")
                        print(f"Nombre: {cliente['nombre']}")
                        print(f"Email: {cliente['email']}")
                        print(f"Teléfono: {cliente['telefono']}")
                        print(f"Dirección: {cliente['direccion']}")
                    else:
                        print("Cliente no encontrado.")
                case "2":
                    numero_tarjeta = input("Número de tarjeta: ")
                    monto = int(input("Monto a recargar: "))
                    nuevo_saldo = actualizar_saldo(numero_tarjeta, monto)
                    print(f"Nuevo saldo: {nuevo_saldo}")
                case "3":
                    numero_tarjeta = input("Número de tarjeta: ")
                    tarjeta = obtener_tarjeta(numero_tarjeta)
                    print(f"Saldo actual: {tarjeta.get('saldo', 'No disponible')}")
                case "4":
                    rutas = obtener_rutas()
                    if rutas:
                        print("\n--- RUTAS REGISTRADAS ---")
                        for ruta in rutas:
                            print(
                                f"ID: {ruta['id']}, Nombre: {ruta['nombre']}, Descripción: {ruta['descripcion']}"
                            )
                    else:
                        print("No hay rutas registradas.")
                case "5":
                    vehiculos = obtener_vehiculos()
                    if vehiculos:
                        print("\n--- VEHÍCULOS DISPONIBLES ---")
                        for vehiculo in vehiculos:
                            print(
                                f"Placa: {vehiculo['placa']}, Marca: {vehiculo['marca']}"
                            )
                    else:
                        print("No hay vehículos disponibles.")
                case "6":
                    print("Saliendo del menú de cliente...")
                    break

        else:
            print("Rol no válido.")
            break


def main():
    role = solicitar_login()
    if role:
        menu(role)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" SISTEMA DE TRANSPORTE API")
    print("=" * 60)
    print(" API:           http://127.0.0.1:8000")
    print(" Documentación: http://127.0.0.1:8000/docs")
    print("=" * 60 + "\n")
    server = threading.Thread(target=desplegar_uvicorn, daemon=True)
    server.start()
    time.sleep(2)
    main()
