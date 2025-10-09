from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

# Dependencias internas del proyecto (Ajustadas a tu estructura)
from session import get_session # Usando tu módulo 'session' para la DB
from repositories.proyecto_repository import ProyectoRepository
from schemas.proyecto import (
    ProyectoCreate, ProyectoRead, ProyectoUpdateEstado, 
    ProyectoUpdateArquitecto
)
from schemas.mueble import MuebleCreate, MuebleRead

# Dependencias de seguridad (Ajustadas a tu estructura)
from core.security import get_current_user 
from models.usuario import Usuario # Modelo de usuario que usas para autenticación

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos (Ventas y Flujo)"]
)

# ----------------------------------------------------------------------
# Dependencias de Autorización
# ----------------------------------------------------------------------

def get_vendedor_o_admin(current_user: Usuario = Depends(get_current_user)):
    """Verifica que el usuario actual tenga rol de Vendedor o Administrador."""
    # Asume que el rol se accede como current_user.rol.nombre
    # Si el rol es una relación, asegúrate de que se cargue
    rol_nombre = current_user.rol.nombre if current_user.rol else None
    
    if rol_nombre not in ["Vendedor", "Administrador", "vendedor", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción. Requerido: Vendedor o Administrador."
        )
    return current_user

def get_admin_o_jefe(current_user: Usuario = Depends(get_current_user)):
    """Verifica que el usuario actual tenga rol de Administrador o Jefe de Proyecto."""
    rol_nombre = current_user.rol.nombre if current_user.rol else None
    
    if rol_nombre not in ["Jefe de Proyecto", "Administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para realizar esta acción. Requerido: Jefe de Proyecto o Administrador."
        )
    return current_user

# ----------------------------------------------------------------------
# 1. CREACIÓN DE PROYECTO (Venta Inicial/Cotización)
# ----------------------------------------------------------------------

@router.post(
    "/", 
    response_model=ProyectoRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Crea una nueva cotización (Proyecto) incluyendo Cliente y Muebles iniciales."
)
def crear_proyecto(
    proyecto_data: ProyectoCreate, 
    db: Session = Depends(get_session),
    # Solo Vendedores o Admins pueden crear proyectos
    current_user: Usuario = Depends(get_vendedor_o_admin) 
):
    """
    Registra una nueva venta/cotización, creando el Cliente, el Proyecto 
    y sus Muebles iniciales. El ID del vendedor se extrae del usuario autenticado.
    """
    repo = ProyectoRepository(db)
    
    # El ID del vendedor es el ID del usuario autenticado
    vendedor_id = current_user.id 
    
    try:
        nuevo_proyecto = repo.create_proyecto(proyecto_data, vendedor_id)
        return nuevo_proyecto
    except Exception as e:
        print(f"Error al crear proyecto: {e}")
        # Retorna un error 400 ya que la validación falló a nivel de DB/lógica de negocio
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar la solicitud: {e}"
        )

# ----------------------------------------------------------------------
# 2. LECTURA Y LISTADO DE PROYECTOS
# ----------------------------------------------------------------------

@router.get(
    "/", 
    response_model=List[ProyectoRead],
    summary="Lista todos los proyectos, opcionalmente filtrados por estado."
)
def listar_proyectos(
    estado: Optional[str] = Query(None, description="Filtrar proyectos por estado (e.g., 'Cotización', 'En Producción')"), 
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user) # Todos los usuarios logueados pueden listar
):
    """Lista todos los proyectos, filtrable por estado."""
    repo = ProyectoRepository(db)
    proyectos = repo.get_proyectos(estado=estado)
    return proyectos

@router.get(
    "/{proyecto_id}", 
    response_model=ProyectoRead,
    summary="Obtiene un proyecto por su ID."
)
def obtener_proyecto(
    proyecto_id: int, 
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user) # Todos los usuarios logueados pueden ver el detalle
):
    """Obtiene los detalles completos de un proyecto específico."""
    repo = ProyectoRepository(db)
    proyecto = repo.get_proyecto_by_id(proyecto_id)
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return proyecto

# ----------------------------------------------------------------------
# 3. ACTUALIZACIONES DE FLUJO (Post-Venta y Producción)
# ----------------------------------------------------------------------

@router.put(
    "/{proyecto_id}/estado", 
    response_model=ProyectoRead,
    summary="Actualiza el estado principal del proyecto."
)
def actualizar_estado_proyecto(
    proyecto_id: int, 
    estado_data: ProyectoUpdateEstado,
    db: Session = Depends(get_session),
    # Solo Jefes de Proyecto o Admins pueden cambiar el estado principal
    current_user: Usuario = Depends(get_admin_o_jefe) 
):
    """Actualiza el estado principal del proyecto (ej: de Cotización a Aprobado o Cerrado)."""
    repo = ProyectoRepository(db)
    proyecto_actualizado = repo.update_estado(proyecto_id, estado_data)
    
    if not proyecto_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
        
    return proyecto_actualizado

@router.post(
    "/{proyecto_id}/mueble", 
    response_model=MuebleRead,
    summary="Añade un mueble nuevo a un proyecto ya existente."
)
def agregar_mueble_adicional(
    proyecto_id: int, 
    mueble_data: MuebleCreate,
    db: Session = Depends(get_session),
    # Requiere Vendedor o Admin (para actualizar la cotización)
    current_user: Usuario = Depends(get_vendedor_o_admin) 
):
    """Añade un mueble nuevo a un proyecto ya existente."""
    repo = ProyectoRepository(db)
    mueble_nuevo = repo.add_mueble_to_proyecto(proyecto_id, mueble_data)

    if not mueble_nuevo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")

    return mueble_nuevo

@router.put(
    "/{proyecto_id}/arquitecto", 
    response_model=ProyectoRead,
    summary="Asigna el jefe de proyecto (arquitecto) responsable."
)
def asignar_arquitecto_proyecto(
    proyecto_id: int, 
    arquitecto_data: ProyectoUpdateArquitecto,
    db: Session = Depends(get_session),
    # Solo Jefes de Proyecto o Admins pueden asignar roles
    current_user: Usuario = Depends(get_admin_o_jefe) 
):
    """Asigna el arquitecto responsable al proyecto."""
    repo = ProyectoRepository(db)
    proyecto_actualizado = repo.assign_arquitecto(proyecto_id, arquitecto_data)
    
    if not proyecto_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto no encontrado")
        
    return proyecto_actualizado
