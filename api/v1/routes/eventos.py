from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session
from session import get_session
from schemas.evento import EventoCalendarioCreate, EventoCalendarioRead
from repositories.evento_repository import EventoRepository

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("/", response_model=EventoCalendarioRead)
def create_evento(data: EventoCalendarioCreate, session: Session = Depends(get_session)):
    return EventoRepository.create(session, data)


@router.get("/", response_model=List[EventoCalendarioRead])
def list_eventos(session: Session = Depends(get_session)):
    return EventoRepository.get_all(session)
