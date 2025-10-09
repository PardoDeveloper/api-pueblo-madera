# create_vendedor.py

from sqlmodel import Session, select
from session import engine
from models.usuario import Usuario, Rol
from core.security import hash_password # Asegúrate de que esta es tu función de hashing
from core.loggin import logger

MAX_BCRYPT_BYTES = 72

def create_vendedor_user():
    """
    Crea un usuario de prueba con el rol 'Vendedor'.
    """
    try:
        with Session(engine) as session:
            # 1. Buscar o Crear el Rol 'Vendedor'
            # 🚨 El nombre del rol debe ser EXACTO al que tu @Depends espera (e.g., "Vendedor" vs "vendedor")
            role_name = "Vendedor" 
            role_stmt = select(Rol).where(Rol.nombre == role_name)
            vendedor_role = session.exec(role_stmt).first()
            
            if not vendedor_role:
                logger.info(f"Creando rol '{role_name}'...")
                vendedor_role = Rol(nombre=role_name)
                session.add(vendedor_role)
                session.commit()
                session.refresh(vendedor_role)

            # 2. Verificar si el usuario ya existe (usaremos 'vendedor' como username)
            username = "vendedor"
            email = "vendedor@pueblomadera.com"
            
            statement = select(Usuario).where(Usuario.username == username)
            existing_user = session.exec(statement).first()

            if not existing_user:
                # 3. Crear el nuevo usuario
                logger.info("Creando usuario VENDEDOR de prueba...")
                
                # Usamos la misma contraseña simple para pruebas
                password_raw = "vendedor123" 
                
                vendedor_user = Usuario(
                    nombre="TestVendedor",
                    username=username,
                    # No necesitamos truncar si la contraseña es corta, pero usamos tu función si existe.
                    hashed_password=hash_password(password_raw), 
                    email=email,
                    activo=True,
                    rol_id=vendedor_role.id
                )
                session.add(vendedor_user)
                session.commit()
                logger.info(f"✅ Usuario VENDEDOR creado: {username} / {password_raw}")
            else:
                logger.info("INFO: Usuario VENDEDOR ya existe.")

    except Exception as e:
        logger.error(f"ERROR AL CREAR USUARIO VENDEDOR: {e}")


if __name__ == "__main__":
    create_vendedor_user()