from sqlmodel import create_engine, Session, SQLModel
<<<<<<< HEAD
from core.loggin import logger
=======
from contextlib import contextmanager

>>>>>>> bfb007c8352752c27eee6438cae3a0d96f19cbd0
# Define el nombre del archivo de la base de datos
sqlite_file_name = "database.db"

# La URL de la base de datos se genera a partir del nombre del archivo
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Crea el motor de la base de datos
# `echo=True` es útil para ver las sentencias SQL que se ejecutan, desactívalo en producción
engine = create_engine(sqlite_url, echo=False, connect_args={"timeout": 30})

<<<<<<< HEAD
=======
def create_database():
    from models.usuario import Usuario, Rol
    from models.cliente import Cliente
    from models.proyecto import Proyecto, Mueble
    
    print("Creando tablas de la base de datos...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas con éxito.")
>>>>>>> bfb007c8352752c27eee6438cae3a0d96f19cbd0

def get_session():
    with Session(engine) as session:
        yield session
