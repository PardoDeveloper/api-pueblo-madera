from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

# Importamos los modelos y esquemas
from models.cliente import Cliente
from models.proyecto import Proyecto, Mueble
from schemas.proyecto import ProyectoCreate, ProyectoUpdateEstado, ProyectoUpdateArquitecto, MuebleCreate

class ProyectoRepository:
    """
    Clase que encapsula la lógica de acceso a datos para Proyectos, Clientes y Muebles.
    Actúa como la única interfaz entre las rutas de FastAPI y la base de datos.
    """

    def __init__(self, db: Session):
        """Inicializa el repositorio con la sesión de la base de datos."""
        self.db = db

    # ----------------------------------------------------
    # 1. CREACIÓN (Venta Inicial/Cotización)
    # ----------------------------------------------------
    def create_proyecto(self, proyecto_data: ProyectoCreate, vendedor_id: int) -> Proyecto:
        """
        Crea un nuevo Cliente, un nuevo Proyecto, y sus Muebles iniciales,
        asegurando que se relacionen correctamente en una única transacción.
        """
        # 1. Crear el modelo Cliente
        cliente_db = Cliente.model_validate(proyecto_data.cliente)
        self.db.add(cliente_db)
        self.db.commit()
        self.db.refresh(cliente_db)
        
        # 2. Crear el modelo Proyecto
        # Usamos los campos de ProyectoBase y asignamos IDs
        proyecto_db = Proyecto(
            nombre_proyecto=proyecto_data.nombre_proyecto,
            fecha_entrega_estimada=proyecto_data.fecha_entrega_estimada,
            cliente_id=cliente_db.id,
            vendedor_id=vendedor_id, # ID del usuario autenticado que realiza la venta
            estado="Cotización" # Estado inicial por defecto
        )
        self.db.add(proyecto_db)
        self.db.commit()
        self.db.refresh(proyecto_db)

        # 3. Crear los modelos Mueble y relacionarlos al Proyecto
        muebles_db = []
        for mueble_schema in proyecto_data.muebles_iniciales:
            # Creamos el Mueble y le asignamos el proyecto_id
            mueble_db = Mueble.model_validate(mueble_schema, update={'proyecto_id': proyecto_db.id})
            muebles_db.append(mueble_db)
        
        self.db.add_all(muebles_db)
        self.db.commit()
        
        # Hacemos refresh del proyecto para asegurar que las relaciones estén cargadas
        self.db.refresh(proyecto_db) 

        # Retornamos el proyecto creado
        return proyecto_db

    # ----------------------------------------------------
    # 2. LECTURA (Consultas)
    # ----------------------------------------------------
    def get_proyecto_by_id(self, proyecto_id: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por su ID."""
        # Se obtienen todas las relaciones (cliente, muebles, etc.) gracias a SQLModel
        statement = select(Proyecto).where(Proyecto.id == proyecto_id)
        return self.db.exec(statement).first()

    def get_proyectos(self, estado: Optional[str] = None) -> List[Proyecto]:
        """Obtiene todos los proyectos, opcionalmente filtrados por estado."""
        statement = select(Proyecto)
        
        if estado:
            statement = statement.where(Proyecto.estado == estado)
            
        # Ordenamos por fecha de creación descendente para mostrar los más nuevos primero
        statement = statement.order_by(Proyecto.fecha_creacion.desc())
        
        return self.db.exec(statement).all()

    # ----------------------------------------------------
    # 3. ACTUALIZACIÓN (Flujo de Trabajo y Asignaciones)
    # ----------------------------------------------------
    def update_estado(self, proyecto_id: int, estado_data: ProyectoUpdateEstado) -> Optional[Proyecto]:
        """Actualiza el estado de un proyecto (ej: de Aprobado a En Producción)."""
        proyecto = self.get_proyecto_by_id(proyecto_id)
        if not proyecto:
            return None
            
        proyecto.estado = estado_data.estado
        
        # Si se cierra el proyecto, registramos la fecha de cierre real
        if estado_data.estado == "Cerrado":
            proyecto.fecha_cierre_real = datetime.utcnow()
            
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto)
        return proyecto
        
    def add_mueble_to_proyecto(self, proyecto_id: int, mueble_data: MuebleCreate) -> Optional[Mueble]:
        """Añade un mueble adicional a un proyecto existente (ej: post-cotización)."""
        # Verificamos si el proyecto existe (get_proyecto_by_id ya lo hace, pero aquí lo necesitamos para el check)
        proyecto = self.db.get(Proyecto, proyecto_id) 
        if not proyecto:
            return None
        
        # Creamos y asignamos el ID del proyecto al nuevo mueble
        mueble_db = Mueble.model_validate(mueble_data, update={'proyecto_id': proyecto_id})
        self.db.add(mueble_db)
        self.db.commit()
        self.db.refresh(mueble_db)
        return mueble_db

    def assign_arquitecto(self, proyecto_id: int, arquitecto_data: ProyectoUpdateArquitecto) -> Optional[Proyecto]:
        """Asigna un arquitecto al proyecto, lo cual es el siguiente paso en el flujo."""
        proyecto = self.get_proyecto_by_id(proyecto_id)
        if not proyecto:
            return None

        proyecto.arquitecto_id = arquitecto_data.arquitecto_id
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto)
        return proyecto

    # Nota: Las funciones para actualizar Muebles individuales (ej: estado_proceso de un mueble)
    # se pueden añadir aquí o en un futuro MuebleRepository.
