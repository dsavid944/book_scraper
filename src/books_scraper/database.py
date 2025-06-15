import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:

    # Gestiona almacenamiento de datos en SQLite.
    # Crea la base de datos si no existe.

    def __init__(self, db_path='src/books_scraper/static/db/books.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def save(self, data, table_name='books'):
        # Recibe lista de dicts y guarda en SQLite.
        df = pd.DataFrame(data)
        hoy = datetime.today().strftime('%Y-%m-%d')
        df['scrape_date'] = hoy
        conn = sqlite3.connect(self.db_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"✅ Guardados {len(df)} registros en {self.db_path}")

    def load(self, table_name='books'):
        # Carga datos de la tabla en un DataFrame.
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df