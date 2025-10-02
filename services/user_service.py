from sqlmodel import Session
from core.security import hash_password, verify_password, create_access_token
from repositories.user_repository import get_user_by_username, create_user
from models.usuario import Usuario

def register_user(db, nombre, username, password, email=None) -> str:
    if get_user_by_username(db, username):
        raise ValueError("Username already registered")
    hashed = hash_password(password)  # ahora segura para bcrypt
    user = create_user(db, nombre, username, hashed, email)
    token = create_access_token({"sub": user.username})
    return token

def login_user(db: Session, username: str, password: str) -> str:
    user: Usuario = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    return create_access_token({"sub": user.username})
