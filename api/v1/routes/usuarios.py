from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from session import get_session
from schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate
from repositories.usuario_repository import UsuarioRepository
from core.security import get_current_user
from models.usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioRead])
def list_usuarios(session: Session = Depends(get_session)):
    return UsuarioRepository.get_all(session)


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(payload: UsuarioCreate, session: Session = Depends(get_session)):
    if UsuarioRepository.get_by_username(session, payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists")
    user = UsuarioRepository.create(
        session,
        username=payload.username,
        password=payload.password,
        email=payload.email,
        nombre=payload.nombre,
        activo=payload.activo,
        rol_id=payload.rol_id,
    )
    return user


@router.get("/{user_id}", response_model=UsuarioRead)
def get_usuario(user_id: int, session: Session = Depends(get_session)):
    user = UsuarioRepository.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return user


@router.put("/{user_id}", response_model=UsuarioRead)
def update_usuario(user_id: int, payload: UsuarioUpdate, session: Session = Depends(get_session)):
    user = UsuarioRepository.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    updated = UsuarioRepository.update(session, user, payload.model_dump(exclude_unset=True))
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(user_id: int, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    # Only allow deletion by admins (simple check based on role name)
    if not current_user or not current_user.rol or current_user.rol.nombre.lower() != "administrador":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    user = UsuarioRepository.get_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    UsuarioRepository.delete(session, user)
    return None
