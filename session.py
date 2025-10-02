from sqlmodel import create_engine, Session, SQLModel

# Define el nombre del archivo de la base de datos
sqlite_file_name = "database.db"

# La URL de la base de datos se genera a partir del nombre del archivo
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Crea el motor de la base de datos
# `echo=True` es útil para ver las sentencias SQL que se ejecutan, desactívalo en producción
engine = create_engine(sqlite_url, echo=True, connect_args={"timeout": 30})

def create_database():
    """
    Crea la base de datos y las tablas a partir de los modelos de SQLModel.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session