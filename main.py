from Scrapers import ashkeebs
import pandas as pd

ash = ashkeebs.Ashkeebs()
ash.get_data()

ashkeebs_data = ash.return_data()

ashkeebs_data.to_csv("csv_files/ashkeebs_data.csv")
print(ashkeebs_data)
