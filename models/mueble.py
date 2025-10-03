from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Mueble(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str 
    descripcion: str 
    precio_estimado: float
    estado_proceso: str = "Esperando Plano" 

    # Relaciones
    # 1. Relación con Proyecto: Clave foránea para saber a qué proyecto pertenece
    proyecto_id: Optional[int] = Field(default=None, foreign_key="proyecto.id")
    proyecto: "Proyecto" = Relationship(back_populates="muebles")

    # 2. Relación con Documentos/Plano: Almacenar la ruta o nombre del archivo PDF
    plano_url: Optional[str] = None # Ruta al archivo PDF del plano
    
    # 3. Relación con Tareas (Pendiente para el módulo de Producción)
    # tareas: List["Tarea"] = Relationship(back_populates="mueble")