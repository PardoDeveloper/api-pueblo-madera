from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from session import get_session
from repositories.mueble_repository import MuebleRepository
from schemas.mueble import MuebleCreate, MuebleRead, MuebleUpdate

router = APIRouter(prefix="/muebles", tags=["Muebles"])


@router.post("/", response_model=MuebleRead, status_code=status.HTTP_201_CREATED)
def create_mueble(data: MuebleCreate, session: Session = Depends(get_session)):
    return MuebleRepository.create(session, data)


@router.get("/", response_model=List[MuebleRead])
def list_muebles(session: Session = Depends(get_session)):
    return MuebleRepository.get_all(session)


@router.get("/{mueble_id}", response_model=MuebleRead)
def get_mueble(mueble_id: int, session: Session = Depends(get_session)):
    mueble = MuebleRepository.get_by_id(session, mueble_id)
    if not mueble:
        raise HTTPException(status_code=404, detail="Mueble no encontrado")
    return mueble


@router.put("/{mueble_id}", response_model=MuebleRead)
def update_mueble(mueble_id: int, data: MuebleUpdate, session: Session = Depends(get_session)):
    mueble = MuebleRepository.get_by_id(session, mueble_id)
    if not mueble:
        raise HTTPException(status_code=404, detail="Mueble no encontrado")
    return MuebleRepository.update(session, mueble, data)


@router.delete("/{mueble_id}")
def delete_mueble(mueble_id: int, session: Session = Depends(get_session)):
    mueble = MuebleRepository.get_by_id(session, mueble_id)
    if not mueble:
        raise HTTPException(status_code=404, detail="Mueble no encontrado")
    MuebleRepository.delete(session, mueble)
    return {"ok": True, "message": "Mueble eliminado correctamente"}
