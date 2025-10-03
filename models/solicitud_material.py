from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class SolicitudMaterial(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tarea_id: int = Field(foreign_key="tarea.id")
    material_id: int = Field(foreign_key="material.id")
    cantidad: float
    estado: str  # pendiente, aprobado, entregado, rechazado
    fecha: datetime = Field(default_factory=datetime.utcnow)
