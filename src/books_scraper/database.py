import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._ruta_db = os.path.join(base_dir, 'static', 'db', 'books.db')
        os.makedirs(os.path.dirname(self._ruta_db), exist_ok=True)

    def guardar(self, datos, nombre_tabla='libros'):
        """Guarda la lista de diccionarios en SQLite."""
        try:
            df = pd.DataFrame(datos)
            df['fecha_extraccion'] = datetime.today().strftime('%Y-%m-%d')
            conn = sqlite3.connect(self._ruta_db)
            df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            conn.close()
            print(f"✅ Guardado en BD {self._ruta_db} ({df.shape[0]} registros)")
        except Exception as e:
            print(f"❌ Error guardando en BD: {e}")

    def cargar(self, nombre_tabla='libros'):
        """Carga datos de SQLite a DataFrame."""
        try:
            conn = sqlite3.connect(self._ruta_db)
            df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
            conn.close()
            print(f"✅ Cargado desde BD ({df.shape[0]} registros)")
            return df
        except Exception as e:
            print(f"❌ Error leyendo de BD: {e}")
            return pd.DataFrame()