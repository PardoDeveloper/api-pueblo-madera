from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.proyecto import Proyecto

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    telefono: str
    direccion: str

    proyectos: List["Proyecto"] = Relationship(back_populates="cliente")
