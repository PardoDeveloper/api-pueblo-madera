from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from session import get_session
from schemas.usuario import UserCreate, UserLogin, Token
from services.user_service import register_user, login_user
from core.security import verify_password, create_access_token
from models.usuario import Usuario
from core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_session)):
    try:
        token = register_user(db, user.nombre, user.username, user.password, user.email)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.username == data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrecta")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def read_current_user(user: Usuario = Depends(get_current_user)):
    return {
        "id": user.id,
        "nombre": user.nombre,
        "username": user.username,
        "email": user.email,
        "activo": user.activo,
        "rol": user.rol.nombre if user.rol else None
    }