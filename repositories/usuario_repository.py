from typing import List, Optional
from sqlmodel import Session, select
from models.usuario import Usuario
from core.security import hash_password
from sqlalchemy.orm import selectinload


class UsuarioRepository:
    @staticmethod
    def get_all(session: Session) -> List[Usuario]:
        statement = select(Usuario).distinct().options(selectinload(Usuario.rol))
        return session.exec(statement).all()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[Usuario]:
        return session.get(Usuario, user_id)

    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[Usuario]:
        statement = select(Usuario).where(Usuario.username == username)
        return session.exec(statement).first()

    @staticmethod
    def create(session: Session, *, username: str, password: str, email: Optional[str] = None, nombre: Optional[str] = None, activo: bool = True, rol_id: Optional[int] = None) -> Usuario:
        hashed = hash_password(password)
        user = Usuario(username=username, email=email, hashed_password=hashed, nombre=nombre or username, activo=activo, rol_id=rol_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, user: Usuario, data: dict) -> Usuario:
        if "password" in data and data["password"]:
            user.hashed_password = hash_password(data["password"])
        for key in ("email", "nombre", "activo", "rol_id"):
            if key in data:
                setattr(user, key, data[key])
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(session: Session, user: Usuario) -> None:
        session.delete(user)
        session.commit()
