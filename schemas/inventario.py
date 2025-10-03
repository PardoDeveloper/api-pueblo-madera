from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
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


# Additional schemas for SolicitudMaterial, Supervision, EventoCalendario, Factura, DetalleFactura
class SolicitudMaterialCreate(SQLModel):
    tarea_id: int
    material_id: int
    cantidad: float


class SolicitudMaterialRead(SQLModel):
    id: int
    tarea_id: int
    material_id: int
    cantidad: float
    estado: str
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)


class SupervisionCreate(SQLModel):
    tarea_id: int
    supervisor_id: int
    estado: str
    observaciones: Optional[str] = None


class SupervisionRead(SQLModel):
    id: int
    tarea_id: int
    supervisor_id: int
    estado: str
    observaciones: Optional[str]
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)


class EventoCalendarioCreate(SQLModel):
    tipo: str
    fecha: datetime
    descripcion: str
    usuario_id: int
    proyecto_id: int


class EventoCalendarioRead(SQLModel):
    id: int
    tipo: str
    fecha: datetime
    descripcion: str
    usuario_id: int
    proyecto_id: int
    model_config = ConfigDict(from_attributes=True)


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
