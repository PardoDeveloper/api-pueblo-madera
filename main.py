from fastapi import FastAPI
from session import create_database, get_session
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """
    Función que maneja los eventos de inicio y apagado de la aplicación.
    """
    print("Iniciando la aplicación...")
    create_database()
    yield
    print("Cerrando la aplicación...")

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

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de PUEBLO MADERA!"}