from sqlmodel import Session, select
from models.tarea import Tarea
from schemas.tarea import TareaCreate, TareaUpdate
from typing import List, Optional

class TareaRepository:

    @staticmethod
    def create(session: Session, data: TareaCreate) -> Tarea:
        tarea = Tarea.from_orm(data)
        session.add(tarea)
        session.commit()
        session.refresh(tarea)
        return tarea

    @staticmethod
    def get_all(session: Session) -> List[Tarea]:
        return session.exec(select(Tarea)).all()

    @staticmethod
    def get_by_id(session: Session, tarea_id: int) -> Optional[Tarea]:
        return session.get(Tarea, tarea_id)

    @staticmethod
    def update(session: Session, tarea: Tarea, data: TareaUpdate) -> Tarea:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(tarea, key, value)
        session.add(tarea)
        session.commit()
        session.refresh(tarea)
        return tarea

    @staticmethod
    def delete(session: Session, tarea: Tarea) -> None:
        session.delete(tarea)
        session.commit()
