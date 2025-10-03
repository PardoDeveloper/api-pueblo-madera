from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyecto_id: int = Field(foreign_key="proyecto.id")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    subtotal: float
    impuestos: float
    total: float
    estado: str  # pendiente, pagada, cancelada


class DetalleFactura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="factura.id")
    concepto: str
    cantidad: int
    precio_unitario: float
    total: float
