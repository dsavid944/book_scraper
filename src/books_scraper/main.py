from book_scraper import BookScraper
from database import DataBase
import pandas as pd
import os


def main():

    scraper = BookScraper()
    bd = DataBase()

    # Obtener datos
    datos = scraper.extraer()

    if datos:
        # Guardar en SQLite
        bd.guardar(datos)

        # Obtener path absoluto del directorio actual
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Ruta donde se guardará el CSV
        output_csv_dir = os.path.join(base_dir, 'static', 'csv')
        os.makedirs(output_csv_dir, exist_ok=True)
        output_csv_path = os.path.join(output_csv_dir, 'books.csv')

        # Convertir a DataFrame y exportar a CSV
        df = pd.DataFrame(datos)
        df.to_csv(output_csv_path, index=False)
        print(f"✅ CSV generado en {output_csv_path}")
        print("✅ Proceso completado")
    else:
        print("❌ No se extrajeron datos")


if __name__ == '__main__':
    main()