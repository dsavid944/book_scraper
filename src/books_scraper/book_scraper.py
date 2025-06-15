import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

class BookScraper:

    def __init__(self):
        self._base = 'http://books.toscrape.com/'
        self._headers = ['Mozilla/5.0', 'Safari/537.36', 'Chrome/91.0']

    # Devuelve una lista con el nombre de cada categoría y el enlace completo donde encontrar los libros.
    def obtener_categorias(self):
        try:
            resp = requests.get(self._base,
                                headers={'User-Agent': random.choice(self._headers)})
            resp.raise_for_status()
        except Exception as e:
            print(f"❌ Error al descargar página principal: {e}")
            return []

        try:
            soup = BeautifulSoup(resp.text, 'html.parser')
            enlaces = soup.select('div.side_categories ul li ul li a')
            cats = []
            for a in enlaces:
                nombre = a.text.strip()
                href = a['href']
                url = urllib.parse.urljoin(self._base, href)
                cats.append((nombre, url))
            return cats
        except Exception as e:
            print(f"❌ Error al parsear categorías: {e}")
            return []

    # Descargar el contenido
    def descargar_pagina(self, url):
        try:
            resp = requests.get(url, headers={'User-Agent': random.choice(self._headers)})
            resp.raise_for_status()
            time.sleep(random.uniform(1,2))
            return resp.text
        except Exception as e:
            # silencio 404 de paginación
            if isinstance(e, requests.HTTPError) and e.response.status_code == 404:
                return None
            print(f"❌ Error descargando {url}: {e}")
            return None

    #  Para cada libro extrae los datos
    def parsear_libros(self, html):
        """Extrae lista de dicts con título, precio y stock de esa página."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            filas = soup.select('article.product_pod')
            lista = []
            for art in filas:
                lista.append({
                    'titulo': art.h3.a['title'],
                    'precio': art.select_one('p.price_color').text,
                    'stock': art.select_one('p.instock.availability').text.strip()
                })
            return lista
        except Exception as e:
            print(f"❌ Error parseando libros: {e}")
            return []

    #  Devuelve la totalidad de libros encontrados.
    def extraer_libros(self):
        """Recorre todas las categorías y sus páginas, devuelve la lista completa."""
        resultado = []
        for cat, url_cat in self.obtener_categorias():
            pagina = 1
            while True:
                url = url_cat if pagina == 1 else url_cat.replace(
                    'index.html', f'page-{pagina}.html'
                )
                html = self.descargar_pagina(url)
                if not html:
                    break
                libros = self.parsear_libros(html)
                if not libros:
                    break
                # añadimos la categoría a cada libro
                for libro in libros:
                    libro['categoria'] = cat
                resultado.extend(libros)
                pagina += 1
        return resultado