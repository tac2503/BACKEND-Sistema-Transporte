
import threading
import time
from app import desplegar_uvicorn

from src.crud import (
    crear_administrador,
    crear_vehiculo, obtener_vehiculos, obtener_vehiculo, eliminar_vehiculo,
    crear_tarjeta, obtener_tarjetas, obtener_tarjeta, eliminar_tarjeta,
    crear_tipo_empleado, obtener_tipos_empleados, obtener_tipo_empleado, eliminar_tipo_empleado,
    crear_cliente, obtener_clientes, obtener_cliente, eliminar_cliente,
    crear_empleado, obtener_empleados, obtener_empleado, eliminar_empleado
)
from src.database.config import SessionLocal
from src.models import Administrador

def menu():
    while True:
        print("1 si es administrador, 2 si es cliente, 0 para salir /n")

        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            db= SessionLocal()
            
            documento =input("Ingrese su documento")
            existe = db.query(Administrador).filter(Administrador.documento == documento).first()
            db.close()
            if existe:
                print("Bienvenido, administrador")
            
                while True:
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
                            
                                admin_nuevo = crear_administrador(
                                    documento=input("Documento: "),
                                    nombre=input("Nombre: "),
                                    email=input("Email: "),
                                    telefono=input("Teléfono: "),
                                    direccion=input("Dirección: ")
                                )
                                print(f"Administrador creado: {admin_nuevo}")
                            
                            
                        case "2":  
                            clientes = obtener_clientes()
                            if clientes:
                                print("\n--- CLIENTES REGISTRADOS ---")
                                for cliente in clientes:
                                    print(f"Documento: {cliente['documento']}, Nombre: {cliente['nombre']}, Email: {cliente['email']}")
                            else:
                                print("No hay clientes registrados.")
                        case "3":  
                            empleados = obtener_empleados()
                            if empleados:
                                print("\n--- EMPLEADOS REGISTRADOS ---")
                                for empleado in empleados:
                                    print(f"Documento: {empleado['documento']}, Nombre: {empleado['nombre']}, Email: {empleado['email']}")
                            else:
                                print("No hay empleados registrados.")
                        case "4":
                            tarjetas = obtener_tarjetas()
                            if tarjetas:
                                print("\n--- TARJETAS REGISTRADAS ---")
                                for tarjeta in tarjetas:
                                    print(f"Número: {tarjeta['numero_tarjeta']}, Cliente: {tarjeta['documento_cliente']}")
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
                                    print(f"Placa: {vehiculo['placa']}, Marca: {vehiculo['marca']}, Ruta ID: {vehiculo['ruta_id']}")
                            else:
                                print("No hay vehículos registrados.")
                        case "7":
                            pass
                        case "8":
                            documento = input("Documento del empleado: ")
                            nombre = input("Nombre del empleado: ")
                            email = input("Email del empleado: ")
                            telefono = input("Teléfono del empleado: ")
                            direccion = input("Dirección del empleado: ")
                            tipo_empleado_id = int(input("ID del tipo de empleado: "))
                            empleado_nuevo = crear_empleado(documento, nombre, email, telefono, direccion, tipo_empleado_id)
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

        elif opcion == "2":
            print("Bienvenido, cliente")
            
            while True:
                print("\nMenú de cliente:")
                print("1.Registrarse como cliente")
                print("2.Ver tarjeta asociada")
                print("3. Recargar tarjeta")
                print("4. Consultar saldo")
                print("5. Ver rutas disponibles")
                print("6. Ver vehiculos disponibles")
                print("7. Salir")
        
        

                cliente_opcion = input("Ingrese su opción: ")
            
                match cliente_opcion:
                    case "1":
                        documento = input("Documento: ")
                        nombre = input("Nombre: ")
                        email = input("Email: ")
                        telefono = input("Teléfono: ")
                        direccion = input("Dirección: ")
                        cliente_nuevo = crear_cliente(documento, nombre, email, telefono, direccion)
                        print(f"Cliente creado: {cliente_nuevo}")
                    case "2":
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
                    case "3":  
                        pass
                    case "4":
                        numero_tarjeta = input("Número de tarjeta: ")
                        tarjeta = obtener_tarjeta(numero_tarjeta)
                        print(f"Saldo actual: {tarjeta.get('saldo', 'No disponible')}")
                    case "5":
                        pass
                    case "6":
                        vehiculos = obtener_vehiculos()
                        if vehiculos:
                            print("\n--- VEHÍCULOS DISPONIBLES ---")
                            for vehiculo in vehiculos:
                                print(f"Placa: {vehiculo['placa']}, Marca: {vehiculo['marca']}")
                        else:
                            print("No hay vehículos disponibles.")
                    case "7":
                        print("Saliendo del menú de cliente...")
                        break
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")  


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
    menu()



