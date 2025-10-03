from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict


class MovimientoBase(SQLModel):
    tipo: str
    cantidad: float
    usuario_id: int
    material_id: Optional[int] = None
    producto_id: Optional[int] = None


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoRead(MovimientoBase):
    id: int
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)
