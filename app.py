from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.config import create_tables
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

def desplegar_uvicorn():
    uvicorn.run(app, host="127.0.0.1", port=8000)
