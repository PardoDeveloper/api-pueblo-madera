# schemas/cliente.py
from sqlmodel import SQLModel
from typing import Optional

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

    class Config:
        orm_mode = True
