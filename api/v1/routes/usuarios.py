from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session, select
from session import get_session
from schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate, ImportExcelResponse
from repositories.usuario_repository import UsuarioRepository
from core.security import get_current_user
from models.usuario import Usuario
import pandas as pd
from sqlalchemy.exc import IntegrityError
from models.usuario import Rol


router = APIRouter(prefix="/usuarios", tags=["usuarios"])

VALID_ROLES = ["administrador", "supervisor", "mueblista", "lijador", "pintor"]

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

@router.post("/import-excel/", response_model=ImportExcelResponse)
def import_usuarios_excel(file: UploadFile = File(...), session: Session = Depends(get_session)):
    try:
        df = pd.read_excel(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Error leyendo el archivo Excel")

    required_columns = {"nombre", "apellido", "email", "rol"}
    if not required_columns.issubset(df.columns.str.lower()):
        raise HTTPException(
            status_code=400,
            detail=f"Excel debe contener las columnas: {', '.join(required_columns)}"
        )

    created_users = []
    skipped_users = []

    for _, row in df.iterrows():
        nombre = str(row.get("nombre", "")).strip()
        apellido = str(row.get("apellido", "")).strip()
        email = str(row.get("email", "")).strip() if row.get("email") else None
        rol_name = str(row.get("rol", "")).strip().lower()

        if rol_name not in VALID_ROLES:
            skipped_users.append({"nombre": f"{nombre} {apellido}", "motivo": "Rol inválido"})
            continue

        # Buscar o crear rol
        rol_obj = session.exec(select(Rol).where(Rol.nombre.ilike(rol_name))).first()
        if not rol_obj:
            rol_obj = Rol(nombre=rol_name)
            session.add(rol_obj)
            session.commit()
            session.refresh(rol_obj)

        # Validar existencia por email primero
        email = str(row.get("email", "")).strip().lower() if row.get("email") else None

        existing_user = None
        if email:
            existing_user = session.exec(select(Usuario).where(Usuario.email == email)).first()

        # Si email no existe, validar por username como fallback
        if not existing_user:
            username = UsuarioRepository._generate_username(session, nombre, apellido)
            existing_user = session.exec(select(Usuario).where(Usuario.username == username)).first()
        else:
            username = existing_user.username  # para reportes

        if existing_user:
            skipped_users.append({"nombre": f"{nombre} {apellido}", "email": email, "motivo": "Ya existe"})
            continue

        # Crear usuario nuevo
        try:
            user = UsuarioRepository.create(
                session,
                username=username,
                password="default123",
                email=email,
                nombre=f"{nombre} {apellido}",
                rol_id=rol_obj.id
            )
            created_users.append(user)
        except Exception:
            session.rollback()
            skipped_users.append({"nombre": f"{nombre} {apellido}", "email": email, "motivo": "Error al crear"})
            continue

    return {
        "creados": created_users,
        "saltados": skipped_users
    }




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
