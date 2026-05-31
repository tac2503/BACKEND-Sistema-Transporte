# BACKEND-Sistema-Transporte

Sistema de informacion para la gestion de un sistema de transporte publico.

El proyecto combina:

- API REST con FastAPI.
- Autenticacion JWT (roles: `admin` y `cliente`).
- Menu interactivo por consola para consumir la API localmente.

## VIDEO FINAL PRUEBAS Y DESPLIEGUE
https://canva.link/27j41tpjk35yufs




## Tecnologias

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL (via `psycopg2-binary`)
- Uvicorn
- HTTPX
- PyJWT
- bcrypt

## Estructura General

- `app.py`: configura FastAPI, registra routers y crea tablas al iniciar.
- `main.py`: levanta el servidor y muestra el menu interactivo (login + operaciones).
- `src/models/`: modelos SQLAlchemy.
- `src/schemas/`: esquemas Pydantic.
- `src/routers/`: endpoints REST.
- `src/crud/`: cliente HTTP para consumir la API desde `main.py`.
- `src/database/config.py`: conexion y sesion SQLAlchemy.
- `src/database/migrate.py`: aplica migraciones SQL pendientes.
- `src/database/seed.py`: crea datos base para desarrollo.

## Modulos De API

Prefijos principales registrados en FastAPI:

- `/auth`
- `/administradores`
- `/clientes`
- `/empleados`
- `/tarjetas`
- `/tipos-empleados`
- `/vehiculos`
- `/rutas`

Consulta interactiva de contratos y ejemplos en:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Requisitos Previos

- Python 3.11 o superior
- PostgreSQL disponible
- `pip` actualizado

## Configuracion Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tac2503/BACKEND-Sistema-Transporte.git
cd BACKEND-Sistema-Transporte
```

### 2. Crear y activar entorno virtual

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```



### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raiz del proyecto:

```env
DATABASE_URL=postgresql+psycopg2://USUARIO:CLAVE@localhost:5432/NOMBRE_BD
JWT_SECRET_KEY=una_clave_larga_y_segura
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Variables obligatorias:

- `DATABASE_URL`
- `JWT_SECRET_KEY`

Variables opcionales (con valor por defecto):

- `JWT_ALGORITHM` (`HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` (`30`)

### 5. Inicializar base de datos (recomendado)

```bash
python -m src.database.migrate
python -m src.database.seed
```

Esto crea/actualiza tablas, aplica migraciones de `src/database/migrations/` y carga datos base para pruebas locales.

## Ejecucion

### Opcion recomendada: API + menu interactivo

```bash
python main.py
```

Expone:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Solo API

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

## Autenticacion y uso del menu

Al iniciar `main.py`, primero se solicita login.

- Login administrador: `POST /auth/login/admin`
- Login cliente: `POST /auth/login/cliente`
- Perfil token actual: `GET /auth/me`

Si ejecutas el seed, puedes usar estas credenciales de desarrollo:

- Admin: documento `1021923966`, contrasena `Admin123!`
- Cliente: documento `12345678`, contrasena `cliente_seguro123`

## Opciones disponibles en consola

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

1. Ver tarjeta asociada
2. Recargar tarjeta
3. Consultar saldo
4. Ver rutas disponibles
5. Ver vehiculos disponibles
6. Salir

## Verificaciones Rapidas

Smoke test de documentacion:

```bash
python smoke_test.py
```

En Windows PowerShell tambien puedes usar:

```powershell
.\run_smoke_test.ps1
```

Validacion de workflow CI:

```bash
python validate_workflow.py
```

## CI

El workflow de GitHub Actions (`.github/workflows/ci_push.yml`) en rama `dev` ejecuta:

<<<<<<< HEAD
```env
DATABASE_URL=postgresql+psycopg2://USUARIO:CLAVE@localhost:5432/NOMBRE_BD
JWT_SECRET_KEY= jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_ALGORITHM=HS256
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
=======
- Lint y formato con Ruff
- Auditoria de dependencias (`pip-audit`)
- Migracion de base de datos
- Seed de datos
- Smoke test de FastAPI
>>>>>>> 82b2ae68c35d9748242b2ce97727b09043164458

## Notas

- La API crea tablas al iniciar (`lifespan` en `app.py`) y adicionalmente soporta migraciones SQL versionadas.
- El cliente HTTP de consola usa `http://localhost:8000` como base URL.

## Desarrollado por

- Tomas Alvarez Castillo
- Miguel Angel Mejia
