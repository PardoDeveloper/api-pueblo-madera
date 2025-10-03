from sqlmodel import SQLModel
from datetime import datetime
from pydantic import ConfigDict


class EventoCalendarioCreate(SQLModel):
    tipo: str
    fecha: datetime
    descripcion: str
    usuario_id: int
    proyecto_id: int


class EventoCalendarioRead(SQLModel):
    id: int
    tipo: str
    fecha: datetime
    descripcion: str
    usuario_id: int
    proyecto_id: int
    model_config = ConfigDict(from_attributes=True)
