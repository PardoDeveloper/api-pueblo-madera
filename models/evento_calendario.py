from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class EventoCalendario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # visita, entrega, instalacion
    fecha: datetime
    descripcion: str
    usuario_id: int = Field(foreign_key="usuario.id")
    proyecto_id: int = Field(foreign_key="proyecto.id")
