from sqlmodel import Session, select
from models.plano import Plano
from schemas.plano import PlanoCreate, PlanoUpdate
from typing import List, Optional

class PlanoRepository:

    @staticmethod
    def create(session: Session, data: PlanoCreate) -> Plano:
        plano = Plano.from_orm(data)
        session.add(plano)
        session.commit()
        session.refresh(plano)
        return plano

    @staticmethod
    def get_all(session: Session) -> List[Plano]:
        return session.exec(select(Plano)).all()

    @staticmethod
    def get_by_id(session: Session, plano_id: int) -> Optional[Plano]:
        return session.get(Plano, plano_id)

    @staticmethod
    def update(session: Session, plano: Plano, data: PlanoUpdate) -> Plano:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(plano, key, value)
        session.add(plano)
        session.commit()
        session.refresh(plano)
        return plano

    @staticmethod
    def delete(session: Session, plano: Plano) -> None:
        session.delete(plano)
        session.commit()
