from sqlmodel import Session, select
from models.solicitud_material import SolicitudMaterial
from schemas.solicitud import SolicitudMaterialCreate
from typing import List, Optional


class SolicitudRepository:
    @staticmethod
    def create(session: Session, data: SolicitudMaterialCreate) -> SolicitudMaterial:
        sol = SolicitudMaterial.from_orm(data)
        session.add(sol)
        session.commit()
        session.refresh(sol)
        return sol

    @staticmethod
    def get_all(session: Session) -> List[SolicitudMaterial]:
        return session.exec(select(SolicitudMaterial)).all()

    @staticmethod
    def get_by_id(session: Session, solicitud_id: int) -> Optional[SolicitudMaterial]:
        return session.get(SolicitudMaterial, solicitud_id)

    @staticmethod
    def approve(session: Session, solicitud_id: int):
        sol = session.get(SolicitudMaterial, solicitud_id)
        if not sol:
            return None
        sol.estado = 'aprobado'
        session.add(sol)
        session.commit()
        session.refresh(sol)
        return sol
