from sqlmodel import Session
from models.movimiento_inventario import MovimientoInventario
from schemas.movimiento import MovimientoCreate
from models.material import Material
from typing import Optional


class MovimientoRepository:
    @staticmethod
    def create(session: Session, data: MovimientoCreate) -> MovimientoInventario:
        movimiento = MovimientoInventario.from_orm(data)
        session.add(movimiento)
        # adjust stock
        if movimiento.material_id:
            mat = session.get(Material, movimiento.material_id)
            if mat:
                if movimiento.tipo == 'entrada':
                    mat.cantidad_disponible += movimiento.cantidad
                else:
                    if mat.cantidad_disponible - movimiento.cantidad < 0:
                        raise ValueError('Stock insuficiente')
                    mat.cantidad_disponible -= movimiento.cantidad
                session.add(mat)
        session.commit()
        session.refresh(movimiento)
        return movimiento
