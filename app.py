from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.config import create_tables
from src.routers import auth_router, administradores_router, tarjeta_router, tipo_empleado_router, vehiculos_router, cliente_router, empleado_router, rutas_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ejecuta tareas de inicio y cierre del ciclo de vida de la API."""
    create_tables()
    yield

app = FastAPI(
    title="Sistema de Transporte API",
    version="1.0.0",docs_url="/docs",
    redoc_url="/redoc", 
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(administradores_router)
app.include_router(cliente_router)
app.include_router(empleado_router)
app.include_router(tarjeta_router)
app.include_router(tipo_empleado_router)
app.include_router(vehiculos_router)
app.include_router(rutas_router)

def desplegar_uvicorn():
    """Inicia el servidor Uvicorn para exponer la API localmente."""
    uvicorn.run(app, host="127.0.0.1", port=8000)
