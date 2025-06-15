from book_scraper import BookScraper
from database import DataBase
import pandas as pd


def main():
    total_pages = 5  # número de páginas a extraer

    scraper = BookScraper(total_pages=total_pages)
    data = scraper.scrape()

    db = DataBase()
    db.save(data)

    # También generar CSV
    df = pd.DataFrame(data)
    csv_path = 'src/books_scraper/static/csv/books.csv'
    df.to_csv(csv_path, index=False)
    print(f"✅ CSV generado en {csv_path}")


if __name__ == '__main__':
    main()