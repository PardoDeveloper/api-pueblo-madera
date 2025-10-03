from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlmodel import Session
from session import get_session
from schemas.factura import FacturaCreate, FacturaRead, DetalleFacturaCreate
from repositories.factura_repository import FacturaRepository

router = APIRouter(prefix="/facturas", tags=["Facturas"])


@router.post("/", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def create_factura(data: FacturaCreate, detalles: List[DetalleFacturaCreate], session: Session = Depends(get_session)):
    try:
        return FacturaRepository.create(session, data, detalles)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
