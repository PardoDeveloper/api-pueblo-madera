from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from session import get_session
from schemas.solicitud import SolicitudMaterialCreate, SolicitudMaterialRead
from repositories.solicitud_repository import SolicitudRepository

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("/", response_model=SolicitudMaterialRead, status_code=status.HTTP_201_CREATED)
def create_solicitud(data: SolicitudMaterialCreate, session: Session = Depends(get_session)):
    return SolicitudRepository.create(session, data)


@router.get("/", response_model=List[SolicitudMaterialRead])
def list_solicitudes(session: Session = Depends(get_session)):
    return SolicitudRepository.get_all(session)


@router.post("/{solicitud_id}/aprobar", response_model=SolicitudMaterialRead)
def aprobar_solicitud(solicitud_id: int, session: Session = Depends(get_session)):
    sol = SolicitudRepository.approve(session, solicitud_id)
    if not sol:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return sol
