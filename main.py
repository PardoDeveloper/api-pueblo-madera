from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import auth, clientes
from api.v1.routes import proyectos, muebles, planos, tareas
from api.v1.routes import materiales, productos, movimientos, solicitudes, supervisiones, eventos, facturas, usuarios
from create_admin import create_admin
from core.loggin import logger
import models
from sqlmodel import SQLModel
from session import engine

@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """
    Función que maneja los eventos de inicio y apagado de la aplicación.
    """
    logger.info("INICIANDO SERVIDOR...")
    SQLModel.metadata.create_all(engine)
    create_admin()
    yield
    logger.info("APAGANDO SERVIDOR...")

app = FastAPI(
    title="API PUEBLO MADERA",
    description="API completo de PUEBLO MADERA",
    version="1.0.0",
    lifespan=lifespan_manager
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(proyectos.router)
app.include_router(muebles.router)
app.include_router(planos.router)
app.include_router(tareas.router)
app.include_router(usuarios.router)
app.include_router(materiales.router)
app.include_router(productos.router)
app.include_router(movimientos.router)
app.include_router(solicitudes.router)
app.include_router(supervisiones.router)
app.include_router(eventos.router)
app.include_router(facturas.router)



@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de PUEBLO MADERA!"}