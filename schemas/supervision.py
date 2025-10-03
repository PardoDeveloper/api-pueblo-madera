from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict


class SupervisionCreate(SQLModel):
    tarea_id: int
    supervisor_id: int
    estado: str
    observaciones: Optional[str] = None


class SupervisionRead(SQLModel):
    id: int
    tarea_id: int
    supervisor_id: int
    estado: str
    observaciones: Optional[str]
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)
