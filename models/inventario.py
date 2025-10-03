from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class SolicitudMaterial(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tarea_id: int = Field(foreign_key="tarea.id")
    material_id: int = Field(foreign_key="material.id")
    cantidad: float
    estado: str  # pendiente, aprobado, entregado, rechazado
    fecha: datetime = Field(default_factory=datetime.utcnow)


class Supervision(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tarea_id: int = Field(foreign_key="tarea.id")
    supervisor_id: int = Field(foreign_key="usuario.id")
    estado: str  # aprobada, rechazada
    observaciones: Optional[str] = None
    fecha: datetime = Field(default_factory=datetime.utcnow)


# ------------------------
# Inventarios
# ------------------------
class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    cantidad_disponible: float
    unidad: str
    stock_minimo: float
    precio_unitario: float


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    cantidad_disponible: int
    precio_unitario: float


class MovimientoInventario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # entrada/salida
    cantidad: float
    fecha: datetime = Field(default_factory=datetime.utcnow)
    usuario_id: int = Field(foreign_key="usuario.id")
    material_id: Optional[int] = Field(default=None, foreign_key="material.id")
    producto_id: Optional[int] = Field(default=None, foreign_key="producto.id")


# ------------------------
# Calendario
# ------------------------
class EventoCalendario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # visita, entrega, instalacion
    fecha: datetime
    descripcion: str
    usuario_id: int = Field(foreign_key="usuario.id")
    proyecto_id: int = Field(foreign_key="proyecto.id")


# ------------------------
# Facturación
# ------------------------
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
