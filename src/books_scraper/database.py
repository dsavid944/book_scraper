import sqlite3
import pandas as pd
import os
from datetime import datetime

class DataBase:

    # Gestiona almacenamiento de datos en SQLite.
    # Crea la base de datos si no existe.
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.rutadb = os.path.join(base_dir, "static", "db", "books.db")


    # Funcion para guarda la informacion
    def guardar(self, datos, nombre_tabla='libros'):
        try:
            df = pd.DataFrame(datos)
            hoy = datetime.today().strftime('%Y-%m-%d')
            df['fecha_extraccion'] = hoy
            conn = sqlite3.connect(self.rutadb)
            df.to_sql(nombre_tabla, conn, if_exists='replace', index=False)
            conn.close()
            print(f"✅ Guardado en base de datos ({df.shape[0]} registros)")
        except Exception as e:
            print(f"❌ Error guardando en BD: {e}")

     # Funcion para Obtener los datos la Bd
    def cargar(self, nombre_tabla='libros'):
        try:
            conn = sqlite3.connect(self.rutadb)
            df = pd.read_sql(f"SELECT * FROM {nombre_tabla}", conn)
            print(f"✅ Cargado desde BD ({df.shape[0]} registros)")
            conn.close()
            return df
        except Exception as e:
            print(f"❌ Error leyendo de BD: {e}")
            return pd.DataFrame()