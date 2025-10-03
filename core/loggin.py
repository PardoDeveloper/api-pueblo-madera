import logging
import sys

# Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.INFO

# Configuración global de logs
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),   # imprime en consola
        logging.FileHandler("app.log", mode="a", encoding="utf-8")  # guarda en archivo
    ]
)

# Logger principal de la app
logger = logging.getLogger("app")

# Reducir verbosidad de SQLAlchemy si molesta
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
