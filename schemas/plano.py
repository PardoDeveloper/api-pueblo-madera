# schemas/plano.py
from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

class PlanoBase(SQLModel):
    archivo_pdf: str
    estado: str

class PlanoCreate(PlanoBase):
    mueble_id: int
    arquitecto_id: int

class PlanoUpdate(SQLModel):
    archivo_pdf: Optional[str] = None
    estado: Optional[str] = None

class PlanoRead(PlanoBase):
    id: int
    mueble_id: int
    arquitecto_id: int
    fecha_subida: datetime

    model_config = ConfigDict(from_attributes=True)
