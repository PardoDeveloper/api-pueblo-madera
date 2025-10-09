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
            print('Ensuring public.cliente.comuna exists...')
            with conn.begin():
                conn.execute(text("ALTER TABLE public.cliente ADD COLUMN IF NOT EXISTS comuna VARCHAR;"))
            print('OK')
        except Exception as e:
            print('Error ensuring comuna:', e)

if __name__ == '__main__':
    run()
