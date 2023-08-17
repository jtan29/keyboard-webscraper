import pandas as pd


class BaseScraper:

    def __init__(self):
        self.frame = pd.DataFrame(columns=["name", "vendor", "price", "type", "store"])

    def get_data(self):
        pass

    def print_data(self):
        print(self.frame)

    def return_data(self):
        return self.frame

    def write_data(self, file_name):
        self.frame.to_csv(file_name)
