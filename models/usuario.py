from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.proyecto import Proyecto

class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)

    usuarios: List["Usuario"] = Relationship(back_populates="rol")


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Optional[str]
    hashed_password: str
    nombre: str
    activo: bool = True
    rol_id: Optional[int] = Field(default=None, foreign_key="rol.id")
    rol: Optional[Rol] = Relationship(back_populates="usuarios")

    proyectos_vendidos: List["Proyecto"] = Relationship(
        back_populates="vendedor",
        sa_relationship_kwargs={"foreign_keys": "Proyecto.vendedor_id"}
    )

    proyectos_jefe: List["Proyecto"] = Relationship(
        back_populates="jefe_proyecto",
        sa_relationship_kwargs={"foreign_keys": "Proyecto.jefe_proyecto_id"}
    )



  

    