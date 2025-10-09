from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from session import engine
from sqlalchemy import text


def run():
    with engine.connect() as conn:
        try:
            print('Altering table mueble: adding columns if not exists...')
            with conn.begin():
                conn.execute(text("ALTER TABLE mueble ADD COLUMN IF NOT EXISTS cantidad INTEGER DEFAULT 1;"))
                conn.execute(text("ALTER TABLE mueble ADD COLUMN IF NOT EXISTS precio_unitario NUMERIC DEFAULT 0;"))
                conn.execute(text("ALTER TABLE mueble ADD COLUMN IF NOT EXISTS categoria VARCHAR;"))
                conn.execute(text("ALTER TABLE mueble ADD COLUMN IF NOT EXISTS incluye_flete BOOLEAN DEFAULT FALSE;"))
            print('OK: mueble columns ensured')
        except Exception as e:
            print('Error altering mueble table:', e)

if __name__ == '__main__':
    run()
    print('Done')
