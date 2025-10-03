from sqlmodel import SQLModel
from typing import Optional
from pydantic import ConfigDict


class MaterialBase(SQLModel):
    nombre: str
    descripcion: str
    cantidad_disponible: float
    unidad: str
    stock_minimo: float
    precio_unitario: float


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad_disponible: Optional[float] = None
    unidad: Optional[str] = None
    stock_minimo: Optional[float] = None
    precio_unitario: Optional[float] = None


class MaterialRead(MaterialBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
