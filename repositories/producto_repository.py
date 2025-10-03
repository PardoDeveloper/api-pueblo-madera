from sqlmodel import Session, select
from models.producto import Producto
from schemas.producto import ProductoCreate
from typing import List, Optional


class ProductoRepository:
    @staticmethod
    def create(session: Session, data: ProductoCreate) -> Producto:
        p = Producto.from_orm(data)
        session.add(p)
        session.commit()
        session.refresh(p)
        return p

    @staticmethod
    def get_all(session: Session) -> List[Producto]:
        return session.exec(select(Producto)).all()

    @staticmethod
    def get_by_id(session: Session, producto_id: int) -> Optional[Producto]:
        return session.get(Producto, producto_id)
