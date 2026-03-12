# BACKEND-Sistema-Transporte

Sistema de informacion para la gestion de un sistema de transporte publico.

El proyecto expone una API con FastAPI y tambien incluye un menu por consola para consumir la API en modo cliente/administrador.

## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL (via `psycopg2-binary`)
- Uvicorn
- HTTPX

## Estructura General

- `app.py`: configura FastAPI, registra routers y crea tablas al iniciar.
- `main.py`: inicia el servidor y muestra el menu interactivo en consola.
- `src/models/`: modelos SQLAlchemy.
- `src/schemas/`: esquemas Pydantic.
- `src/routers/`: endpoints REST.
- `src/crud/`: cliente HTTP para consumir la API desde `main.py`.
- `src/database/config.py`: conexion a base de datos y sesion SQLAlchemy.

## Opciones Disponibles En El Menu

Al ejecutar `main.py`, se habilitan dos perfiles: administrador y cliente.

### Administrador

1. Crear administradores
2. Ver clientes
3. Ver empleados
4. Ver tarjetas
5. Ver tipos de empleados
6. Ver vehiculos
7. Ver rutas
8. Registrar empleado
9. Crear tarjeta
10. Crear tipo de empleado
11. Crear vehiculo
12. Salir

### Cliente

1. Registrarse como cliente
2. Ver tarjeta asociada
3. Recargar tarjeta (actualizar saldo)
4. Consultar saldo
5. Ver rutas disponibles
6. Ver vehiculos disponibles
7. Salir

## Ejecucion Local

### 1. Clonar y entrar al proyecto

```bash
git clone https://github.com/tac2503/BACKEND-Sistema-Transporte.git
cd BACKEND-Sistema-Transporte
```

### 2. Crear entorno virtual

En Windows (PowerShell):

```powershell
python -m venv venv
.\.venv\Scripts\Activate.ps1
```



### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raiz del proyecto con:

```env
DATABASE_URL=postgresql+psycopg2://USUARIO:CLAVE@localhost:5432/NOMBRE_BD
```

Nota: Esta URL se saca directamente desde NEON.

### 5. Ejecutar el proyecto

Opcion recomendada para usar menu + API:

```bash
python main.py
```

Esto levanta:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Ejecucion Solo API (opcional)

Si solo quieres levantar la API:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## Notas

- Las tablas se crean automaticamente al iniciar la API (en `lifespan` con `create_tables()`).
- El menu de `main.py` consume la API por HTTP en `http://localhost:8000`.

## Desarrollado por:
 - Tomás Álvarez Castillo
 - Miguel Angel Mejía
