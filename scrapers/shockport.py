from bs4 import BeautifulSoup
from scrapers import base
import requests
import pandas as pd

vendors = ['KBDFans', 'Akko', 'ePBT', 'PBTFans', 'Shockport+Keyboards', 'Tai-Hao', 'The+Right+PC', 'XMI']


class Shockport(base.BaseScraper):
    def __init__(self):
        super().__init__()

    def get_data(self):
        for v in vendors:
            url = "https://shockport.ca/collections/in-stock-keycap-sets?filter.p.vendor=" + v
            html_data = requests.get(url).text
            soup = BeautifulSoup(html_data, 'html5lib')
            products = soup.find_all('div', class_="grid-product__content")
            for item in products:
                title = item.find('div', class_='grid-product__title grid-product__title--body').text
                price = item.find('div', class_='grid-product__price').find('span', class_='money').text
                product_type = "keycaps"
                data = [[title, v, price, product_type, "Shockport"]]
                temp_frame = pd.DataFrame(data, columns=["name", "vendor", "price", "type", "store"])
                temp_frame['price'] = temp_frame['price'].replace(r'\s+|\\n|CAD|\$', ' ', regex=True)
                temp_frame['name'] = temp_frame['name'].replace(r'\s+|\\n', ' ', regex=True)
                temp_frame['vendor'] = temp_frame['vendor'].replace(r'\s+|\\n', ' ', regex=True)
                temp_frame['store'] = temp_frame['store'].replace(r'\s+|\\n', ' ', regex=True)
                self.frame = pd.concat([self.frame, temp_frame], ignore_index=True)
