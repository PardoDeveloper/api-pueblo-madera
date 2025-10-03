from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from models.mueble import Mueble


class Plano(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    mueble_id: int = Field(foreign_key="mueble.id")
    arquitecto_id: int = Field(foreign_key="usuario.id")
    archivo_pdf: str
    estado: str  # pendiente, enviado, aprobado, rechazado
    fecha_subida: datetime = Field(default_factory=datetime.utcnow)

    mueble: "Mueble" = Relationship(back_populates="planos")