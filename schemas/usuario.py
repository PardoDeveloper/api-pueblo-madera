from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    nombre: str
    username: str
    password: str
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
# --- Additional CRUD schemas (kept separate from the lightweight auth models above) ---
class UsuarioCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    nombre: Optional[str] = None
    activo: Optional[bool] = True
    rol_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class RolRead(BaseModel):
    id: int
    nombre: str

    model_config = ConfigDict(from_attributes=True)



class UsuarioRead(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    nombre: Optional[str] = None
    activo: bool
    rol_id: Optional[int] = None
    rol: Optional[RolRead] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioReadBasic(BaseModel):
    id: int
    nombre: Optional[str] = None
    email: Optional[str] = None

    
    model_config = ConfigDict(from_attributes=True)


class UsuarioUpdate(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    password: Optional[str] = None
    activo: Optional[bool] = None
    rol_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioImportado(BaseModel):
    id: int
    username: str
    email: Optional[str]
    nombre: str
    activo: bool
    rol_id: Optional[int]

    class Config:
        orm_mode = True

class ImportExcelResponse(BaseModel):
    creados: List[UsuarioImportado]
    saltados: List[dict]  # lista de dict con nombre, email y motivo