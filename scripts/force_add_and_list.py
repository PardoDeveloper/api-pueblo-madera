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
            print('Running ALTER TABLE to add comuna (if not exists)')
            with conn.begin():
                conn.execute(text("ALTER TABLE public.cliente ADD COLUMN IF NOT EXISTS comuna VARCHAR;"))
            print('ALTER executed')
        except Exception as e:
            print('ALTER error:', e)

        try:
            print('\nListing columns from pg_attribute for public.cliente:')
            res = conn.execute(text("SELECT attname FROM pg_attribute WHERE attrelid = 'public.cliente'::regclass AND attnum > 0 AND NOT attisdropped ORDER BY attnum;"))
            rows = res.fetchall()
            for r in rows:
                print('-', r[0])
        except Exception as e:
            print('Error listing pg_attribute:', e)

if __name__ == '__main__':
    run()
