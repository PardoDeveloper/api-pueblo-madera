from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# Importamos Cliente (no causa bucle con Proyecto)
from models.cliente import Cliente

# NO importamos 'Usuario' aquí, usamos la cadena de texto "Usuario" 
# en las relaciones para evitar el error de importación circular.

class Mueble(SQLModel, table=True):
    """
    Representa un mueble individual que forma parte de un proyecto.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    precio_estimado: float
    estado_proceso: str = "Esperando Plano" # El estado de producción del mueble
    
    # Relación Many-to-One con Proyecto
    proyecto_id: Optional[int] = Field(default=None, foreign_key="proyecto.id")
    proyecto: "Proyecto" = Relationship(back_populates="muebles")


class Proyecto(SQLModel, table=True):
    """
    Representa la venta/cotización principal que inicia el flujo de trabajo.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_proyecto: str
    
    # Control de estado de la venta/proyecto
    estado: str = "Cotización" # Ej: Cotización, Aprobado, En Producción, Cerrado
    
    # Fechas importantes
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_entrega_estimada: Optional[datetime] = None
    fecha_cierre_real: Optional[datetime] = None
    
    # ----------------------------------------------------
    # RELACIONES
    # ----------------------------------------------------

    # 1. Cliente (Many-to-One)
    cliente_id: int = Field(foreign_key="cliente.id")
    cliente: Cliente = Relationship(back_populates="proyectos")
    
    # 2. Vendedor (Many-to-One con Usuario - Usamos string para romper el ciclo)
    vendedor_id: int = Field(foreign_key="usuario.id")
    vendedor: "Usuario" = Relationship(
        back_populates="proyectos_vendidos",
        sa_relationship_kwargs={"lazy": "joined"}
    )
    
    # 3. Muebles (One-to-Many)
    muebles: List["Mueble"] = Relationship(back_populates="proyecto")
    
    # 4. Arquitecto Asignado (Optional, Many-to-One con Usuario - Usamos string)
    arquitecto_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    arquitecto: Optional["Usuario"] = Relationship(
        back_populates="proyectos_disenados",
        sa_relationship_kwargs={"lazy": "joined"}
    )