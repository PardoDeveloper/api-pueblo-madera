from sqlmodel import create_engine, Session, SQLModel
from core.loggin import logger

# Define el nombre del archivo de la base de datos
sqlite_file_name = "database.db"

# La URL de la base de datos se genera a partir del nombre del archivo
sqlite_url = f"sqlite:///{sqlite_file_name}"


# Datos de conexión (usa tus valores reales)
POSTGRES_USER = "db_pueblo_madera_user"
POSTGRES_PASSWORD = "HMm2npdyPSO8eq1J4YOLk3TJ770JjQIm"
POSTGRES_HOST = "dpg-d3j779mmcj7s739o2pvg-a"       # ej. "localhost" o "db.myserver.com"
POSTGRES_PORT = "5432"          # puerto por defecto
POSTGRES_DB = "db_pueblo_madera"

# URL de conexión (usa el driver psycopg2)
postgres_url = "postgresql://db_pueblo_madera_user:HMm2npdyPSO8eq1J4YOLk3TJ770JjQIm@dpg-d3j779mmcj7s739o2pvg-a.oregon-postgres.render.com/db_pueblo_madera"

# Crea el motor de la base de datos
# `echo=True` es útil para ver las sentencias SQL que se ejecutan, desactívalo en producción

# engine = create_engine(postgres_url, echo=False, connect_args={"timeout": 30}) #SQLITE3
engine = create_engine(postgres_url, echo=False) # PostgrSql


def get_session():
    with Session(engine) as session:
        yield session
