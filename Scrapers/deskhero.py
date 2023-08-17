from bs4 import BeautifulSoup
import requests
from Scrapers import base
import pandas as pd




class Deskhero(base.BaseScraper):
    def __init__(self):
        super().__init__()

    def get_data(self):
        for i in range(1, 14):
            url = "https://www.deskhero.ca/collections/keycap-sets?page=" + str(i) + "&grid_list=grid-view"
            html_data = requests.get(url).text
            soup = BeautifulSoup(html_data, 'html5lib')
            products = soup.find_all('div', class_="productitem")
            for item in products:
                title = item.find('h2', class_='productitem--title').text
                vendor = item.find('span', class_='productitem--vendor').find('a').text
                price = item.find('div', class_='productitem__price').find('span',
                                                                           class_='money price__compare-at--max').text
                product_type = "keycaps"
                data = [[title, vendor, price, product_type, "DeskHero"]]
                temp_frame = pd.DataFrame(data, columns=["name", "vendor", "price", "type", "store"])
                temp_frame['price'] = temp_frame['price'].replace(r'\s+|\\n|CAD|\$', ' ', regex=True)
                temp_frame['name'] = temp_frame['name'].replace(r'\s+|\\n', ' ', regex=True)
                self.frame = pd.concat([self.frame, temp_frame], ignore_index=True)
