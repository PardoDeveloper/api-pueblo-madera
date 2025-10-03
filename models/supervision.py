from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Supervision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tarea_id: int = Field(foreign_key="tarea.id")
    supervisor_id: int = Field(foreign_key="usuario.id")
    estado: str  # aprobada, rechazada
    observaciones: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)
