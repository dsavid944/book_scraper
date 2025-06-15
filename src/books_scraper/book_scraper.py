import requests
from bs4 import BeautifulSoup
import time
import random

class BookScraper:

    URL_BASE = 'http://books.toscrape.com/catalogue/page-{}.html'

    def __init__(self, total_paginas=1):
            self.total_paginas = total_paginas
            self.lista_headers = [
                'Mozilla/5.0', 'Safari/537.36', 'Chrome/91.0'
        ]

    def obtener_pagina(self, numero_pagina):
        headers = {'User-Agent': random.choice(self.lista_headers)}
        url = self.URL_BASE.format(numero_pagina)
        respuesta = requests.get(url, headers=headers)
        if respuesta.status_code != 200:
            raise ConnectionError(f"Error al acceder a {url}")
        time.sleep(random.uniform(1, 3))
        return respuesta.text

    def parsear_libros(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        breadcrumb = soup.select_one('ul.breadcrumb')
        migas = breadcrumb.find_all('li') if breadcrumb else []
        categoria_pagina = migas[-1].text.strip() if migas else 'Desconocida'

        articulos = soup.select('article.product_pod')
        libros = []
        for art in articulos:
            titulo = art.h3.a['title']
            precio = art.select_one('p.price_color').text
            stock = art.select_one('p.instock.availability').text.strip()
            categoria = categoria_pagina
            libros.append({
                'titulo': titulo,
                'precio': precio,
                'stock': stock,
                'categoria': categoria
            })
        return libros

    # Recorre todas las páginas y devuelve una lista de registros.
    def extraer(self):
        lista_total = []
        for pagina in range(1, self.total_paginas + 1):
            html = self.obtener_pagina(pagina)
            libros = self.parsear_libros(html)
            lista_total.extend(libros)
        return lista_total