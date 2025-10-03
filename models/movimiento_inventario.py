from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class MovimientoInventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # entrada/salida
    cantidad: float
    fecha: datetime = Field(default_factory=datetime.utcnow)
    usuario_id: int = Field(foreign_key="usuario.id")
    material_id: Optional[int] = Field(default=None, foreign_key="material.id")
    producto_id: Optional[int] = Field(default=None, foreign_key="producto.id")
