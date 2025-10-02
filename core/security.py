from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from models.usuario import Usuario
from session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY = "mi_clave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_BYTES = 72

def hash_password(password: str) -> str:
    # Codifica en bytes y corta a 72 bytes
    truncated_bytes = password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    truncated = truncated_bytes.decode("utf-8", "ignore")
    return pwd_context.hash(truncated)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    truncated_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    truncated = truncated_bytes.decode("utf-8", "ignore")
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    # Recuperamos TODO el usuario de la base de datos
    statement = select(Usuario).where(Usuario.username == username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user