from sqlmodel import Session, select
from models.evento_calendario import EventoCalendario
from schemas.evento import EventoCalendarioCreate
from typing import List


class EventoRepository:
    @staticmethod
    def create(session: Session, data: EventoCalendarioCreate) -> EventoCalendario:
        ev = EventoCalendario.from_orm(data)
        session.add(ev)
        session.commit()
        session.refresh(ev)
        return ev

    @staticmethod
    def get_all(session: Session) -> List[EventoCalendario]:
        return session.exec(select(EventoCalendario)).all()
