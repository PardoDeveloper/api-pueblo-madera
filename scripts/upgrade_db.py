import sys
from pathlib import Path
# Ensure project root is on sys.path so 'session' can be imported
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import text
from session import engine


def run():
    with engine.connect() as conn:
        # 1) Add comuna column if not exists (Postgres)
        try:
            print('Adding columna comuna to cliente if not exists...')
            conn.execute(text("ALTER TABLE cliente ADD COLUMN IF NOT EXISTS comuna VARCHAR;"))
            print('OK: comuna column ensured')
        except Exception as e:
            print('Error adding comuna column:', e)

        # 2) Create pago table if not exists
        try:
            print('Creating table pago if not exists...')
            conn.execute(text('''
                CREATE TABLE IF NOT EXISTS pago (
                    id SERIAL PRIMARY KEY,
                    proyecto_id INTEGER REFERENCES proyecto(id),
                    factura_id INTEGER REFERENCES factura(id),
                    tipo TEXT,
                    metodo_pago TEXT,
                    banco TEXT,
                    monto NUMERIC,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            '''))
            print('OK: pago table ensured')
        except Exception as e:
            print('Error creating pago table:', e)


if __name__ == '__main__':
    run()
    print('Upgrade finished')
