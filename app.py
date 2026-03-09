from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.config import create_tables
from src.routers import administradores_router, tarjeta_router, tipo_empleado_router, vehiculos_router
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="Sistema de Transporte API",
    version="1.0.0",docs_url="/docs",
    redoc_url="/redoc", 
    lifespan=lifespan
)

app.include_router(administradores_router)
app.include_router(tarjeta_router)
app.include_router(tipo_empleado_router)
app.include_router(vehiculos_router)

def desplegar_uvicorn():
    uvicorn.run(app, host="127.0.0.1", port=8000)
