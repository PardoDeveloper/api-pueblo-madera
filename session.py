import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel
from core.loggin import logger

load_dotenv()

# Define el nombre del archivo de la base de datos
sqlite_file_name = "database.db"

# La URL de la base de datos se genera a partir del nombre del archivo
sqlite_url = f"sqlite:///{sqlite_file_name}"

# URL de conexión desde variable de entorno
postgres_url = os.getenv("DATABASE_URL", "postgresql://db_pueblo_madera_user:HMm2npdyPSO8eq1J4YOLk3TJ770JjQIm@dpg-d3j779mmcj7s739o2pvg-a.oregon-postgres.render.com/db_pueblo_madera")

# Crea el motor de la base de datos
# `echo=True` es útil para ver las sentencias SQL que se ejecutan, desactívalo en producción

# engine = create_engine(postgres_url, echo=False, connect_args={"timeout": 30}) #SQLITE3
engine = create_engine(postgres_url, echo=False) # PostgrSql


def get_session():
    with Session(engine) as session:
        yield session
