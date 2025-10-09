from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

# Importamos los modelos de la base de datos
from models.cliente import Cliente
from models.proyecto import Proyecto
from models.mueble import Mueble

# Importamos el schema de creación (que incluye ClienteCreate y MuebleCreate)
from schemas.proyecto import ProyectoCreate, ProyectoUpdateEstado, ProyectoUpdateArquitecto, ProyectoRead
from schemas.mueble import MuebleCreate

class ProyectoRepository:
    """
    Clase que encapsula la lógica de acceso a datos para Proyectos, Clientes y Muebles.
    Maneja la lógica de negocio para la creación de cotizaciones anidadas.
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
        
        try:
            # 1. CREAR EL CLIENTE
            cliente_db = Cliente(**proyecto_data.cliente.model_dump())
            self.db.add(cliente_db)
            self.db.commit()
            self.db.refresh(cliente_db)
            
            # 2. CREAR EL PROYECTO
            proyecto_fields = proyecto_data.model_dump(exclude={"cliente", "muebles_iniciales", "estado"})
            
            proyecto_db = Proyecto(
                **proyecto_fields,
                cliente_id=cliente_db.id,       # Asignamos el ID del cliente recién creado
                vendedor_id=vendedor_id,        # ID del usuario autenticado que realiza la venta
                estado="Cotización",            # Forzamos el estado inicial
            )
            self.db.add(proyecto_db)
            self.db.commit()
            self.db.refresh(proyecto_db)

            # 3. CREAR LOS MUEBLES INICIALES
            muebles_db = []
            for mueble_schema in proyecto_data.muebles_iniciales:
                mueble_fields = mueble_schema.model_dump()
                
                mueble_db = Mueble(
                    **mueble_fields, 
                    proyecto_id=proyecto_db.id,
                )
                
                muebles_db.append(mueble_db)
            
            self.db.add_all(muebles_db)
            self.db.commit()
            
            self.db.refresh(proyecto_db) 

            return proyecto_db

        except Exception as e:
            # En caso de error, hacemos rollback para asegurar la consistencia de la DB
            self.db.rollback()
            raise e

    # ----------------------------------------------------
    # 2. LECTURA (Consultas)
    # ----------------------------------------------------
    def get_proyecto_by_id(self, proyecto_id: int) -> Optional[Proyecto]:
        """Obtiene un proyecto por su ID."""
        statement = select(Proyecto).where(Proyecto.id == proyecto_id)
        return self.db.exec(statement).first()

    def get_proyectos(self, estado: Optional[str] = None) -> List[Proyecto]:
        """Obtiene todos los proyectos, opcionalmente filtrados por estado."""
        statement = select(Proyecto)
        
        if estado:
            statement = statement.where(Proyecto.estado == estado)
            
        # Ordenamos por ID descendente (asumiendo que ID es auto-incremental y refleja la creación)
        statement = statement.order_by(Proyecto.id.desc())
        
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
        
        # Si el proyecto se marca como finalizado o cerrado, registra la fecha de fin real
        if estado_data.estado in ["Finalizado", "Cerrado"]:
            # Usamos fecha_fin_real del modelo Proyecto
            proyecto.fecha_fin_real = datetime.utcnow()
            
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto)
        return proyecto
        
    def add_mueble_to_proyecto(self, proyecto_id: int, mueble_data: MuebleCreate) -> Optional[Mueble]:
        """Añade un mueble adicional a un proyecto existente (ej: post-cotización)."""
        # Verificamos si el proyecto existe
        proyecto = self.db.get(Proyecto, proyecto_id) 
        if not proyecto:
            return None
        
        # Creamos y asignamos el ID del proyecto al nuevo mueble
        mueble_db = Mueble(**mueble_data.model_dump(), proyecto_id=proyecto_id)
        
        self.db.add(mueble_db)
        self.db.commit()
        self.db.refresh(mueble_db)
        return mueble_db

    def assign_arquitecto(self, proyecto_id: int, arquitecto_data: ProyectoUpdateArquitecto) -> Optional[Proyecto]:
        """Asigna un jefe de proyecto (arquitecto) al proyecto."""
        proyecto = self.get_proyecto_by_id(proyecto_id)
        if not proyecto:
            return None

        # Nota: Asumo que el campo en el modelo Proyecto es 'jefe_proyecto_id' o 'arquitecto_id'
        # Usaré 'jefe_proyecto_id' que es el que definimos en ProyectoCreate
        proyecto.jefe_proyecto_id = arquitecto_data.arquitecto_id
        
        self.db.add(proyecto)
        self.db.commit()
        self.db.refresh(proyecto)
        return proyecto
