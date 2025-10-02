from sqlmodel import Session, select
from models.usuario import Usuario

def get_user_by_username(db: Session, username: str) -> Usuario | None:
    statement = select(Usuario).where(Usuario.username == username)
    return db.exec(statement).first()

def create_user(db: Session, nombre: str, username: str, hashed_password: str, email: str | None = None) -> Usuario:
    user = Usuario(nombre=nombre, username=username, password_hash=hashed_password, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user