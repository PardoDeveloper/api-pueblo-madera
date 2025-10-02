from pydantic import BaseModel

class UserCreate(BaseModel):
    nombre: str
    username: str
    password: str
    email: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
