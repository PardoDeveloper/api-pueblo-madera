from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from session import engine
from sqlalchemy import text


def run():
    with engine.connect() as conn:
        print('Connected to:', conn.engine.url)

        def list_columns(table_name):
            print(f"\nColumns for {table_name}:")
            try:
                res = conn.execute(text(f"select column_name, data_type from information_schema.columns where table_name='{table_name}';"))
                rows = res.fetchall()
                if not rows:
                    print(' - No columns returned (table may not exist in this schema)')
                else:
                    for r in rows:
                        print(' -', r[0], r[1])
            except Exception as e:
                print(' Error listing columns for', table_name, e)

        list_columns('cliente')
        list_columns('mueble')

        # Search for specific columns across all tables
        try:
            print('\nSearching for columns named "comuna" or "cantidad" across all tables:')
            res = conn.execute(text("select table_schema, table_name, column_name from information_schema.columns where column_name in ('comuna','cantidad') order by table_schema, table_name;"))
            rows = res.fetchall()
            if not rows:
                print(' - none found')
            else:
                for r in rows:
                    print(' -', r[0], r[1], r[2])
        except Exception as e:
            print(' Error searching for columns:', e)

if __name__ == '__main__':
    run()
