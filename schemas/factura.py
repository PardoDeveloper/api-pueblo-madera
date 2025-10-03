from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict


class FacturaCreate(SQLModel):
    proyecto_id: int
    subtotal: float
    impuestos: float
    total: float
    estado: str


class FacturaRead(SQLModel):
    id: int
    proyecto_id: int
    fecha: datetime
    subtotal: float
    impuestos: float
    total: float
    estado: str
    model_config = ConfigDict(from_attributes=True)


class DetalleFacturaCreate(SQLModel):
    factura_id: int
    concepto: str
    cantidad: int
    precio_unitario: float
    total: float


class DetalleFacturaRead(SQLModel):
    id: int
    factura_id: int
    concepto: str
    cantidad: int
    precio_unitario: float
    total: float
    model_config = ConfigDict(from_attributes=True)
