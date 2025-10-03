from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Cliente(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_completo: str
    email: str = Field(index=True)
    telefono: str
    direccion_instalacion: str 
    
    # Relación inversa: Un cliente puede tener muchos proyectos (cotizaciones/ventas)
    proyectos: List["Proyecto"] = Relationship(back_populates="cliente")