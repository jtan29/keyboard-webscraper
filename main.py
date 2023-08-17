from Scrapers import ashkeebs, deskhero, oneofzero, shockport
import pandas as pd

ash = ashkeebs.Ashkeebs()
dh = deskhero.Deskhero()
ooz = oneofzero.OneOfZero()
sp = shockport.Shockport()

ash.get_data()
dh.get_data()
ooz.get_data()
sp.get_data()



ashkeebs_data = ash.return_data()
deskhero_data = dh.return_data()
oneofzero_data = ooz.return_data()
shockport_data = sp.return_data()

ashkeebs_data.to_csv("csv_files/ashkeebs_data.csv")
deskhero_data.to_csv("csv_files/deskhero_data.csv")
oneofzero_data.to_csv("csv_files/oneofzero_data.csv")
shockport_data.to_csv("csv_files/shockport_data.csv")


canadian_data = pd.concat([ashkeebs_data, deskhero_data, oneofzero_data, shockport_data], ignore_index=True)
print(canadian_data)
canadian_data.to_csv("csv_files/canadian_keycaps.csv")
