from sqlmodel import Session, select
from models.mueble import Mueble
from schemas.mueble import MuebleCreate, MuebleUpdate
from typing import List, Optional

class MuebleRepository:

    @staticmethod
    def create(session: Session, data: MuebleCreate) -> Mueble:
        mueble = Mueble.from_orm(data)
        session.add(mueble)
        session.commit()
        session.refresh(mueble)
        return mueble

    @staticmethod
    def get_all(session: Session) -> List[Mueble]:
        return session.exec(select(Mueble)).all()

    @staticmethod
    def get_by_id(session: Session, mueble_id: int) -> Optional[Mueble]:
        return session.get(Mueble, mueble_id)

    @staticmethod
    def update(session: Session, mueble: Mueble, data: MuebleUpdate) -> Mueble:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(mueble, key, value)
        session.add(mueble)
        session.commit()
        session.refresh(mueble)
        return mueble

    @staticmethod
    def delete(session: Session, mueble: Mueble) -> None:
        session.delete(mueble)
        session.commit()
