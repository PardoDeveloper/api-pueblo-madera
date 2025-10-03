from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from session import get_session
from schemas.movimiento import MovimientoCreate, MovimientoRead
from repositories.movimiento_repository import MovimientoRepository

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])


@router.post("/", response_model=MovimientoRead, status_code=status.HTTP_201_CREATED)
def create_movimiento(data: MovimientoCreate, session: Session = Depends(get_session)):
    try:
        return MovimientoRepository.create(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
