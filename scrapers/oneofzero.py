from bs4 import BeautifulSoup
import requests
from scrapers import base
import pandas as pd


class OneOfZero(base.BaseScraper):
    def __init__(self):
        super().__init__()

    def get_data(self):
        for i in range(1, 3):
            url = "https://oneofzero.net/collections/keycaps?page=" + str(i)
            html_data = requests.get(url).text
            soup = BeautifulSoup(html_data, 'html5lib')
            products = soup.find_all('div', class_="grid-item grid-product")
            for item in products:
                title = item.find('div', class_='grid-product__title').text
                vendor = item.find('div', class_='grid-product__vendor').text
                price = item.find('span', class_='grid-product__price--current').find('span',
                                                                                      class_='visually-hidden').text
                product_type = 'keycaps'
                data = [[title, vendor, price, product_type, "ONEofZERO"]]
                temp_frame = pd.DataFrame(data, columns=["name", "vendor", "price", "type", "store"])
                temp_frame['price'] = temp_frame['price'].replace(r'\s+|\\n|CAD|\$', ' ', regex=True)
                temp_frame['name'] = temp_frame['name'].replace(r'\s+|\\n', ' ', regex=True)
                temp_frame['vendor'] = temp_frame['vendor'].replace(r'\s+|\\n', ' ', regex=True)
                temp_frame['store'] = temp_frame['store'].replace(r'\s+|\\n', ' ', regex=True)
                self.frame = pd.concat([self.frame, temp_frame], ignore_index=True)
