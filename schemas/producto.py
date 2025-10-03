from sqlmodel import SQLModel
from pydantic import ConfigDict


class ProductoBase(SQLModel):
    nombre: str
    descripcion: str
    cantidad_disponible: int
    precio_unitario: float


class ProductoCreate(ProductoBase):
    pass


class ProductoRead(ProductoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
