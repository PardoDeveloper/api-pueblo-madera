from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from session import get_session
from schemas.supervision import SupervisionCreate, SupervisionRead
from repositories.supervision_repository import SupervisionRepository

router = APIRouter(prefix="/supervisiones", tags=["Supervisiones"])


@router.post("/", response_model=SupervisionRead, status_code=status.HTTP_201_CREATED)
def create_supervision(data: SupervisionCreate, session: Session = Depends(get_session)):
    return SupervisionRepository.create(session, data)
