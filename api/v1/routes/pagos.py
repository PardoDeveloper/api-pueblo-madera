from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session, select
from session import get_session
from models.pago import Pago

router = APIRouter(prefix="/pagos", tags=["Pagos"])


@router.post("/", response_model=Pago, status_code=status.HTTP_201_CREATED)
def create_pago(pago: Pago, session: Session = Depends(get_session)):
    try:
        session.add(pago)
        session.commit()
        session.refresh(pago)
        return pago
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Pago])
def list_pagos(session: Session = Depends(get_session)):
    statement = select(Pago).order_by(Pago.id.desc())
    return session.exec(statement).all()
