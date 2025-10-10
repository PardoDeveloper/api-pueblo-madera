from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from session import get_session
from repositories.plano_repository import PlanoRepository
from schemas.plano import PlanoCreate, PlanoRead, PlanoUpdate
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/planos", tags=["Planos"])


@router.post("/", response_model=PlanoRead, status_code=status.HTTP_201_CREATED)
def create_plano(data: PlanoCreate, session: Session = Depends(get_session)):
    try:
        return PlanoRepository.create(session, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[PlanoRead])
def list_planos(session: Session = Depends(get_session)):
    return PlanoRepository.get_all(session)


@router.get("/by-mueble/{mueble_id}", response_model=PlanoRead)
def get_plano_by_mueble(mueble_id: int, session: Session = Depends(get_session)):
    plano = PlanoRepository.get_by_mueble_id(session, mueble_id)
    if not plano:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano no encontrado para este mueble")
    return plano


@router.get("/{plano_id}", response_model=PlanoRead)
def get_plano(plano_id: int, session: Session = Depends(get_session)):
    plano = PlanoRepository.get_by_id(session, plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano no encontrado")
    return plano


@router.put("/{plano_id}", response_model=PlanoRead)
def update_plano(plano_id: int, data: PlanoUpdate, session: Session = Depends(get_session)):
    plano = PlanoRepository.get_by_id(session, plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano no encontrado")
    return PlanoRepository.update(session, plano, data)


@router.delete("/{plano_id}")
def delete_plano(plano_id: int, session: Session = Depends(get_session)):
    plano = PlanoRepository.get_by_id(session, plano_id)
    if not plano:
        raise HTTPException(status_code=404, detail="Plano no encontrado")
    PlanoRepository.delete(session, plano)
    return {"ok": True, "message": "Plano eliminado correctamente"}
