from sqlmodel import Session, select
from session import engine
from models.usuario import Usuario
from core.security import hash_password

MAX_BCRYPT_BYTES = 72  # bcrypt solo soporta hasta 72 bytes

def truncate_password(password: str) -> str:
    """
    Trunca el password a 72 bytes para bcrypt, evitando errores con UTF-8.
    """
    truncated_bytes = password.encode("utf-8")[:MAX_BCRYPT_BYTES]
    return truncated_bytes.decode("utf-8", "ignore")


def create_admin():
    try:
        with Session(engine) as session:
            # Buscar si el admin ya existe
            statement = select(Usuario).where(Usuario.username == "admin")
            admin = session.exec(statement).first()
            if admin:
                print("Usuario administrador ya existe.")
                return

            # Crear usuario admin con password truncado
            password = truncate_password("Admin123")
            admin_user = Usuario(
                nombre="Administrador",
                username="admin",
                password_hash=hash_password(password),
                email="admin@example.com",
                activo=True,
                rol_id=None
            )
            session.add(admin_user)
            session.commit()
            print("Usuario administrador creado con username 'admin' y password 'Admin123'")

    except Exception as e:
        print("Error al crear el administrador:", e)


if __name__ == "__main__":
    create_admin()
