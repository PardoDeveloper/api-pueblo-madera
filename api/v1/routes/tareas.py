from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from session import get_session
from repositories.tarea_repository import TareaRepository
from schemas.tarea import TareaCreate, TareaRead, TareaUpdate

router = APIRouter(prefix="/tareas", tags=["Tareas"])


@router.post("/", response_model=TareaRead, status_code=status.HTTP_201_CREATED)
def create_tarea(data: TareaCreate, session: Session = Depends(get_session)):
    return TareaRepository.create(session, data)


@router.get("/", response_model=List[TareaRead])
def list_tareas(session: Session = Depends(get_session)):
    return TareaRepository.get_all(session)


@router.get("/{tarea_id}", response_model=TareaRead)
def get_tarea(tarea_id: int, session: Session = Depends(get_session)):
    tarea = TareaRepository.get_by_id(session, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.put("/{tarea_id}", response_model=TareaRead)
def update_tarea(tarea_id: int, data: TareaUpdate, session: Session = Depends(get_session)):
    tarea = TareaRepository.get_by_id(session, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return TareaRepository.update(session, tarea, data)


@router.delete("/{tarea_id}")
def delete_tarea(tarea_id: int, session: Session = Depends(get_session)):
    tarea = TareaRepository.get_by_id(session, tarea_id)
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    TareaRepository.delete(session, tarea)
    return {"ok": True, "message": "Tarea eliminada correctamente"}
