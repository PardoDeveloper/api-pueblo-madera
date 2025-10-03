from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


from models.proyecto import Proyecto 

class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)

    usuarios: List["Usuario"] = Relationship(back_populates="rol")


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    username: str = Field(unique=True, index=True)
    email: Optional[str] = Field(unique=True)
    password_hash: str
    activo: bool = True
    rol_id: Optional[int] = Field(default=None, foreign_key="rol.id")

    rol: Optional["Rol"] = Relationship(back_populates="usuarios")

    # Relaciones con Proyecto
    proyectos_vendidos: List[Proyecto] = Relationship(
        back_populates="vendedor", 
        sa_relationship_kwargs={"primaryjoin": "Usuario.id == Proyecto.vendedor_id"}
    )
    proyectos_disenados: List[Proyecto] = Relationship(
        back_populates="arquitecto", 
        sa_relationship_kwargs={"primaryjoin": "Usuario.id == Proyecto.arquitecto_id"}
    )