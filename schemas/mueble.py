# schemas/mueble.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# --- 1. MuebleBase (Base para todos los esquemas, incluye campos de cotización) ---
class MuebleBase(SQLModel):
    nombre: str
    descripcion: str
    
    # CAMPOS DE COTIZACIÓN ENVIADOS POR EL FRONT-END
    cantidad: int = Field(default=1, gt=0)
    precio_unitario: float = Field(default=0.0, ge=0)
    # Campos opcionales que puede enviar el frontend
    categoria: Optional[str] = None
    incluye_flete: Optional[bool] = False
    
    # CAMPOS DEL FLUJO DE TRABAJO (Con valores por defecto para no ser requeridos)
    estado: str = "Cotización"  # Valor por defecto
    fecha_inicio: datetime = Field(default_factory=datetime.utcnow)
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None


# --- 2. MuebleCreate (Usado para POST /proyectos/) ---
# Hereda todos los campos de MuebleBase. No requiere redefinir nada,
# ya que MuebleBase maneja los valores por defecto y el repositorio asigna proyecto_id.
class MuebleCreate(MuebleBase):
    pass


# --- 3. MuebleUpdate (Para modificar un mueble existente) ---
class MuebleUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None
    
    estado: Optional[str] = None
    fecha_fin_estimada: Optional[datetime] = None
    fecha_fin_real: Optional[datetime] = None


# --- 4. MuebleRead (Usado para retornar información al front) ---
class MuebleRead(MuebleBase):
    id: int
    proyecto_id: int  # Aquí se incluye la clave foránea

    model_config = ConfigDict(from_attributes=True)