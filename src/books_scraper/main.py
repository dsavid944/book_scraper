from book_scraper import BookScraper
from database import DataBase
import pandas as pd
import os

def main():
    raspador = BookScraper()
    bd = DataBase()

    datos = raspador.extraer_libros()
    if not datos:
        print("❌ No se extrajeron datos")
        return

    # Guardar en SQLite
    bd.guardar(datos)

    # Exportar a CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(base_dir, 'static', 'csv')
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, 'books.csv')

    try:
        df = pd.DataFrame(datos)
        df.to_csv(csv_path, index=False)
        print(f"✅ CSV generado en {csv_path}")
    except Exception as e:
        print(f"❌ Error al guardar CSV: {e}")

    print("✅ Proceso completado")

if __name__ == '__main__':
    main()