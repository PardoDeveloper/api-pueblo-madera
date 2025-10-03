# schemas/cliente.py
from sqlmodel import SQLModel
from typing import Optional
from pydantic import ConfigDict

class ClienteBase(SQLModel):
    nombre: str
    correo: str
    telefono: str
    direccion: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(SQLModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteRead(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
