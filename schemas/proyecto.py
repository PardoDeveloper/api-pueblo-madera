# schemas/proyecto.py
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

class ProyectoBase(SQLModel):
    estado: str
    fecha_fin_estimada: Optional[datetime] = None
    total_estimado: float = 0.0
    total_final: float = 0.0

class ProyectoCreate(ProyectoBase):
    cliente_id: int
    vendedor_id: int
    jefe_proyecto_id: int

class ProyectoUpdate(SQLModel):
    estado: Optional[str] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    total_estimado: Optional[float] = None
    total_final: Optional[float] = None

class ProyectoRead(ProyectoBase):
    id: int
    cliente_id: int
    vendedor_id: int
    jefe_proyecto_id: int
    fecha_inicio: datetime
    fecha_fin_real: Optional[datetime]

    class Config:
        orm_mode = True
