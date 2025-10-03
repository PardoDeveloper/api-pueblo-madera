from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from session import get_session
from repositories.material_repository import MaterialRepository
from schemas.material import MaterialCreate, MaterialRead, MaterialUpdate

router = APIRouter(prefix="/materiales", tags=["Materiales"])


@router.post("/", response_model=MaterialRead, status_code=status.HTTP_201_CREATED)
def create_material(data: MaterialCreate, session: Session = Depends(get_session)):
    return MaterialRepository.create(session, data)


@router.get("/", response_model=List[MaterialRead])
def list_materiales(session: Session = Depends(get_session)):
    return MaterialRepository.get_all(session)


@router.get("/{material_id}", response_model=MaterialRead)
def get_material(material_id: int, session: Session = Depends(get_session)):
    m = MaterialRepository.get_by_id(session, material_id)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return m


@router.put("/{material_id}", response_model=MaterialRead)
def update_material(material_id: int, data: MaterialUpdate, session: Session = Depends(get_session)):
    m = MaterialRepository.get_by_id(session, material_id)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return MaterialRepository.update(session, m, data)


@router.delete("/{material_id}")
def delete_material(material_id: int, session: Session = Depends(get_session)):
    m = MaterialRepository.get_by_id(session, material_id)
    if not m:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    MaterialRepository.delete(session, m)
    return {"ok": True}
