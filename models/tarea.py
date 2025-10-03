from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.mueble import Mueble

class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mueble_id: int = Field(foreign_key="mueble.id")
    maestro_id: int = Field(foreign_key="usuario.id")
    tipo: str  # armado, lijado, pintura, embalado, instalacion
    estado: str  # pendiente, en_progreso, completada, validada
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    evidencia: Optional[str] = None

    mueble: "Mueble" = Relationship(back_populates="tareas")