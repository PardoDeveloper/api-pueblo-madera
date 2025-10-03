from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import auth, clientes
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
<<<<<<< HEAD
app.include_router(clientes.router)
=======
app.include_router(auth.router, prefix="/api/v1") # Recomendación: Añadir prefix para consistencia
# AÑADIR: Inclusión del router de proyectos
app.include_router(proyectos.router, prefix="/api/v1")
>>>>>>> bfb007c8352752c27eee6438cae3a0d96f19cbd0

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de PUEBLO MADERA!"}