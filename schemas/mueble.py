# schemas/mueble.py
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class MuebleBase(SQLModel):
    nombre: str
    descripcion: str
    estado: str
    fecha_inicio: Optional[datetime] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None

class MuebleCreate(MuebleBase):
    proyecto_id: int

class MuebleUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None

class MuebleRead(MuebleBase):
    id: int
    proyecto_id: int

    class Config:
        orm_mode = True
