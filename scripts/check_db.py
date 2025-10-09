from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from session import engine

def run():
    with engine.connect() as conn:
        print('Connected to:', conn.engine.url)
        # Check columns in cliente
        from sqlalchemy import text
        try:
            res = conn.execute(text("select column_name, data_type from information_schema.columns where table_name='cliente';"))
            rows = res.fetchall()
            if not rows:
                print('No columns returned for table cliente. Table may not exist in this schema.')
            else:
                print('Columns for cliente:')
                for r in rows:
                    print('-', r[0], r[1])
        except Exception as e:
            print('Error querying information_schema:', e)
        # Additionally, list tables named cliente across schemas
        try:
            res2 = conn.execute(text("select table_schema, table_name from information_schema.tables where table_name='cliente';"))
            trows = res2.fetchall()
            print('\nTables named cliente found:')
            for t in trows:
                print('-', t[0], t[1])
        except Exception as e:
            print('Error listing tables:', e)

        # Search for column comuna across all tables
        try:
            res3 = conn.execute(text("select table_schema, table_name from information_schema.columns where column_name='comuna';"))
            crows = res3.fetchall()
            print('\nAny columns named comuna:')
            if not crows:
                print(' - none found')
            else:
                for c in crows:
                    print('-', c[0], c[1])
        except Exception as e:
            print('Error searching for comuna:', e)

if __name__ == '__main__':
    run()
