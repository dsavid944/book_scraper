import requests
from bs4 import BeautifulSoup
import time
import random

class BookScraper:

    BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

    def __init__(self, total_pages=1):
        self.total_pages = total_pages
        self.headers_list = [
            'Mozilla/5.0', 'Safari/537.36', 'Chrome/91.0'
        ]

    def fetch_page(self, page_number):
        headers = {'User-Agent': random.choice(self.headers_list)}
        url = self.BASE_URL.format(page_number)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(f"Error al acceder a {url}")
        # Pausa aleatoria para no sobrecargar el servidor
        time.sleep(random.uniform(1, 3))
        return response.text

    def parse_books(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.select('article.product_pod')
        books = []
        for art in articles:
            title = art.h3.a['title']
            price = art.select_one('p.price_color').text
            stock = art.select_one('p.instock.availability').text.strip()
            category = art.find_previous('ul', class_='breadcrumb').find_all('li')[2].a.text
            books.append({
                'title': title,
                'price': price,
                'stock': stock,
                'category': category
            })
        return books

    def scrape(self):
        # Recorre todas las páginas y devuelve una lista de registros.
        all_books = []
        for page in range(1, self.total_pages + 1):
            html = self.fetch_page(page)
            books = self.parse_books(html)
            all_books.extend(books)
        return all_books