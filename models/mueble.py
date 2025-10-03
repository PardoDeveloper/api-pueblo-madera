from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.tarea import Tarea
    from models.plano import Plano
    from models.proyecto import Proyecto
    

class Mueble(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id")
    nombre: str
    descripcion: str
    estado: str  # diseño, armado, lijado, pintado, embalado, entregado
    fecha_inicio: Optional[datetime] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None

    proyecto: "Proyecto" = Relationship(back_populates="muebles")
    planos: List["Plano"] = Relationship(back_populates="mueble")
    tareas: List["Tarea"] = Relationship(back_populates="mueble")