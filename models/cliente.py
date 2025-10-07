from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.proyecto import Proyecto

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Identificación Única (Crucial)
    # RUT (Rol Único Tributario o Cédula de Identidad)x
    rut: str = Field(index=True, unique=True)
    
    # Información Personal
    nombre: str
    apellido_paterno: Optional[str] = None # Útil para separación de nombres
    apellido_materno: Optional[str] = None # Útil para una búsqueda más precisa

    # Contacto
    correo: str = Field(unique=True) # El correo debe ser único
    telefono: Optional[str]
    
    # Domicilio
    direccion: Optional[str]
    
    # Relación con otros modelos
    proyectos: List["Proyecto"] = Relationship(back_populates="cliente")

    # Mantenemos la relación existente
    # proyectos: List["Proyecto"] = Relationship(back_populates="cliente")