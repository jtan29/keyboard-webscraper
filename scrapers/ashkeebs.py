from bs4 import BeautifulSoup
import requests
import pandas as pd
from scrapers import base


class Ashkeebs(base.BaseScraper):
    def __init__(self):
        super().__init__()

    def get_data(self):
        for i in range(1, 4):
            url = "https://www.ashkeebs.com/product-category/keycaps/page/" + str(i) + "/?currency=CAD&product_count=36"
            html_data = requests.get(url).text
            soup = BeautifulSoup(html_data, 'html5lib')
            product_page = soup.find('ul',
                                     class_="fusion-grid fusion-grid-3 fusion-flex-align-items-flex-start "
                                            "fusion-grid-posts-cards")
            products = product_page.find_all('li')
            for item in products:
                title = item.find('h3').find('a').text
                vendor = title
                price = item.find('span', class_='woocommerce-Price-amount amount').find('bdi').text
                product_type = 'keycaps'
                data = [[title, vendor, price, product_type, "Ashkeebs"]]
                temp_frame = pd.DataFrame(data, columns=["name", "vendor", "price", "type", "store"])
                temp_frame['price'] = temp_frame['price'].replace(r'\s+|\\n|CAD|\$', ' ', regex=True)
                temp_frame['name'] = temp_frame['name'].replace(r'\s+|\\n', ' ', regex=True)
                self.frame = pd.concat([self.frame, temp_frame], ignore_index=True)
