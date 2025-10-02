from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Rol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str

    # Se usa string "Usuario" para referenciar la clase
    usuarios: List["Usuario"] = Relationship(back_populates="rol")


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    username: str = Field(unique=True, index=True)
    email: Optional[str] = None
    password_hash: str
    activo: bool = True
    rol_id: Optional[int] = Field(default=None, foreign_key="rol.id")

    # Se usa string "Rol" para referenciar la clase
    rol: Optional["Rol"] = Relationship(back_populates="usuarios")
