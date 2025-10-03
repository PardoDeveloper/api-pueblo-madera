from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from models.cliente import Cliente
    from models.mueble import Mueble

class Proyecto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    vendedor_id: int = Field(foreign_key="usuario.id")
    jefe_proyecto_id: int = Field(foreign_key="usuario.id")

    estado: str  # cotizacion, produccion, instalacion, cerrado
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None

    total_estimado: float = 0.0
    total_final: float = 0.0

    cliente: "Cliente" = Relationship(back_populates="proyectos")
    muebles: List["Mueble"] = Relationship(back_populates="proyecto")