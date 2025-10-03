# schemas/tarea.py
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class TareaBase(SQLModel):
    tipo: str
    estado: str
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    evidencia: Optional[str] = None

class TareaCreate(TareaBase):
    mueble_id: int
    maestro_id: int

class TareaUpdate(SQLModel):
    tipo: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    evidencia: Optional[str] = None

class TareaRead(TareaBase):
    id: int
    mueble_id: int
    maestro_id: int

    class Config:
        orm_mode = True
