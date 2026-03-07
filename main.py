
import threading
import time
from app import desplegar_uvicorn
import requests

def menu():
    while True:
        print("1 si es administrador, 2 si es cliente, 0 para salir /n")

        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            print("Bienvenido, administrador")
            
            while True:
                print("\nMenú de administrador:")
                print("1. Ver clientes")
                print("2. Ver empleados")
                print("3. Ver tarjetas")
                print("4. Ver tipos de empleados")
                print("5. Ver vehículos")
                print("6. Ver rutas")
                print("7. Registrar empleado")
                print("8. Salir")

                admin_opcion = input("Ingrese su opción: ")
            
                match admin_opcion:
                    case "1":
                        pass
                    case "2":
                        pass
                    case "3":  
                        pass
                    case "4":
                        pass
                    case "5":
                        pass
                    case "6":
                        pass
                    case "7":
                        pass
                    case "8":
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
                        pass
                    case "2":
                        pass
                    case "3":  
                        pass
                    case "4":
                        pass
                    case "5":
                        pass
                    case "6":
                        pass
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
    server = threading.Thread(target=desplegar_uvicorn(), daemon=True)
    server.start()
    time.sleep(1.5)
    menu()



