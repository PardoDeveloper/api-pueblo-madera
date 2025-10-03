from sqlmodel import Session
from models.factura import Factura, DetalleFactura


class FacturaRepository:
    @staticmethod
    def create(session: Session, factura_data, detalles_data: list) -> Factura:
        factura = Factura.from_orm(factura_data)
        session.add(factura)
        session.commit()
        session.refresh(factura)
        for ddata in detalles_data:
            det = DetalleFactura.from_orm(ddata)
            det.factura_id = factura.id
            session.add(det)
        session.commit()
        session.refresh(factura)
        return factura
