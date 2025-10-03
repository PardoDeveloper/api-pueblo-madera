from typing import Optional
from sqlmodel import SQLModel, Field


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    cantidad_disponible: int
    precio_unitario: float
