from sqlmodel import SQLModel
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict

# Importamos los schemas anidados para la creación del proyecto
from schemas.cliente import ClienteCreate, ClienteRead # Asume que está en schemas/cliente.py
from schemas.mueble import MuebleCreate, MuebleRead # Asume que está en schemas/mueble.py
from schemas.usuario import UsuarioReadBasic
class ProyectoBase(SQLModel):
    # Campos que vienen directamente del Proyecto Model
    estado: str # Siempre será "Cotización" al crear
    fecha_fin_estimada: Optional[datetime] = None
    total_estimado: float = 0.0
    total_final: float = 0.0

class ProyectoCreate(ProyectoBase):
    """
    Schema usado para recibir el payload de una nueva cotización desde el front-end.
    Contiene objetos anidados para crear el Cliente y los Muebles en una sola transacción.
    """
    # Campo requerido para la lógica de negocio (ID del Arquitecto/Jefe de Proyecto)
    jefe_proyecto_id: int 
    
    # 1. Objeto Cliente para crear (usando el schema de Cliente)
    cliente: ClienteCreate 
    
    # 2. Lista de Muebles iniciales para crear (usando el schema de Mueble)
    muebles_iniciales: List[MuebleCreate] 
    
    # Nota: vendedor_id se inyecta desde el token del usuario autenticado en el endpoint.
    # Nota: cliente_id se genera después de crear el cliente en el repositorio.
    
class ProyectoUpdateEstado(SQLModel):
    estado: str

class ProyectoUpdateArquitecto(SQLModel):
    arquitecto_id: int

class ProyectoUpdate(SQLModel):
    estado: Optional[str] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None
    total_estimado: Optional[float] = None
    total_final: Optional[float] = None

class ProyectoRead(ProyectoBase):
    """Schema para leer y retornar un proyecto, incluyendo los IDs de las relaciones."""
    id: int
    cliente: ClienteRead
    vendedor: UsuarioReadBasic # El usuario que vende
    jefe_proyecto: UsuarioReadBasic # El usuario que es jefe/arquitecto
    muebles: List[MuebleRead]
    fecha_inicio: datetime
    fecha_fin_real: Optional[datetime]

    # Configuración de Pydantic para manejar los objetos ORM de SQLModel
    model_config = ConfigDict(from_attributes=True)
