from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict


class SolicitudMaterialCreate(SQLModel):
    tarea_id: int
    material_id: int
    cantidad: float


class SolicitudMaterialRead(SQLModel):
    id: int
    tarea_id: int
    material_id: int
    cantidad: float
    estado: str
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)
