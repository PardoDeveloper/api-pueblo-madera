from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Pago(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proyecto_id: Optional[int] = Field(default=None, foreign_key="proyecto.id")
    factura_id: Optional[int] = Field(default=None, foreign_key="factura.id")
    tipo: str = Field(default="abono")  # 'pago_inicial' o 'abono'
    metodo_pago: Optional[str] = None
    banco: Optional[str] = None
    monto: float = 0.0
    fecha: datetime = Field(default_factory=datetime.utcnow)
