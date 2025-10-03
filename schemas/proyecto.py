from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

# Base para creación y actualización (lo que se puede modificar/enviar)
class MuebleBase(SQLModel):
    nombre: str
    descripcion: str
    precio_estimado: float

# Esquema de Entrada (Input)
class MuebleCreate(MuebleBase):
    pass

# Esquema de Salida (Output) - Lo que se muestra al usuario
class MuebleRead(MuebleBase):
    id: int
    estado_proceso: str
    plano_url: Optional[str] = None
    proyecto_id: int

#CLIENTE
# Base para creación y actualización
class ClienteBase(SQLModel):
    nombre_completo: str
    email: str
    telefono: str
    direccion_instalacion: str

# Esquema de Entrada (Input)
class ClienteCreate(ClienteBase):
    pass

# Esquema de Salida (Output)
class ClienteRead(ClienteBase):
    id: int
    # No mostramos la lista de proyectos aquí para evitar referencias circulares complejas

#PROYECTO
# Base para creación y actualización
class ProyectoBase(SQLModel):
    nombre_proyecto: str
    fecha_entrega_estimada: Optional[datetime] = None
    # No incluimos IDs aquí, se manejan en la creación/actualización

# Esquema de Entrada (Input) - Para crear un nuevo Proyecto/Cotización
class ProyectoCreate(ProyectoBase):
    # Cuando creas un proyecto, necesitas los datos del cliente
    cliente: ClienteCreate
    
    # También la información inicial de los muebles que se están cotizando
    muebles_iniciales: list[MuebleCreate]

# Esquema de Salida (Output) - El detalle completo de un proyecto
class ProyectoRead(ProyectoBase):
    id: int
    estado: str
    fecha_creacion: datetime
    fecha_cierre_real: Optional[datetime] = None
    
    # Incluimos los datos del cliente y los muebles
    cliente: ClienteRead
    muebles: list[MuebleRead]
    
    # IDs de los usuarios involucrados (los nombres se obtendrán con JOINs o lookups)
    vendedor_id: int
    arquitecto_id: Optional[int] = None

# Esquema para actualizar el estado del Proyecto
class ProyectoUpdateEstado(SQLModel):
    estado: str # Nuevo estado (ej: "Aprobado por Cliente", "En Producción")

# Esquema para actualizar el Arquitecto asignado (puede ser en otra ruta/esquema)
class ProyectoUpdateArquitecto(SQLModel):
    arquitecto_id: int