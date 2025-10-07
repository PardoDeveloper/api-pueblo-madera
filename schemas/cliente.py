from sqlmodel import SQLModel
from typing import Optional, List
from pydantic import ConfigDict

class ClienteBase(SQLModel):
    rut: str
    nombre: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(SQLModel):
    rut: Optional[str] = None
    nombre: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None


class ClienteRead(ClienteBase):
    id: int

    # Configuración de Pydantic para manejar los objetos ORM de SQLModel
    model_config = ConfigDict(from_attributes=True)