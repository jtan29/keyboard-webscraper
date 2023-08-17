import pandas as pd
import streamlit as st
from Scrapers import shockport, oneofzero, deskhero, ashkeebs
from PIL import Image
from plotnine import *

canadian_keycaps = pd.DataFrame(columns=["name", "vendor", "price", "type", "store"])

app_mode = st.sidebar.selectbox("Select Page", ["Info", "Retrieve Data", "View Dataset"])

if app_mode == "Info":
    st.title("Keycaps: an introduction")
    st.markdown("On mechanical keyboards, keycaps sit on top of the switch stem and form the surface that is"
                " in direct contact with the fingers. Keycaps can affect the typing experience through the material's "
                "texture as well "
                "as affecting the sound from the switches bottoming out. The design of the keycaps is also an important"
                " contributor to the overall aesthetics of the keyboard."
                " This page examines the pricing of keycap sets offered by four different small-to-medium sized "
                "enthusiast "
                "mechanical keyboard vendors in Canada:")
    st.markdown("* [Ashkeebs](https://www.ashkeebs.com/)")
    st.markdown("* [Deskhero](https://www.deskhero.ca/)")
    st.markdown("* [ONEofZERO](https://oneofzero.net/)")
    st.markdown("* [Shockport Keyboards](https://shockport.ca/)")
    image = Image.open("images/Key_cap_grab_bag_from_Signature_Plastics_(25275100714).jpg")
    st.image(image, caption="Assorted keycaps from a Signature Plastics grab bag")
    st.markdown("Image credit: Brett Spangler from Austin, US, "
                "[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0), via Wikimedia Commons")

if app_mode == "Retrieve Data":
    ash = st.checkbox("Ashkeebs")
    dh = st.checkbox("Deskhero")
    ooz = st.checkbox("ONEofZERO")
    sp = st.checkbox("Shockport Keyboards")
    reset_button = st.button("Reset stored data")
    if reset_button:
        canadian_keycaps = pd.DataFrame(columns=["name", "vendor", "price", "type", "store"])
        canadian_keycaps.to_csv("csv_files/canadian_keycaps.csv")
    scrape_button = st.button("Retrieve data")
    if scrape_button:
        toPrint = []
        with st.spinner("Scraping..."):
            if ash:
                toPrint.append("Ashkeebs")
                ash_obj = ashkeebs.Ashkeebs()
                ash_obj.get_data()
                ashkeebs_data = ash_obj.return_data()
                canadian_keycaps = pd.concat([canadian_keycaps, ashkeebs_data])
            if dh:
                toPrint.append("Deskhero")
                dh_obj = deskhero.Deskhero()
                dh_obj.get_data()
                deskhero_data = dh_obj.return_data()
                canadian_keycaps = pd.concat([canadian_keycaps, deskhero_data])
            if ooz:
                toPrint.append("ONEofZERO")
                ooz_obj = oneofzero.OneOfZero()
                ooz_obj.get_data()
                oneofzero_data = ooz_obj.return_data()
                canadian_keycaps = pd.concat([canadian_keycaps, oneofzero_data])
            if sp:
                toPrint.append("Shockport Keyboards")
                sp_obj = shockport.Shockport()
                sp_obj.get_data()
                shockport_data = sp_obj.return_data()
                canadian_keycaps = pd.concat([canadian_keycaps, shockport_data])

            st.markdown("Finished. Selected vendors:")
            for i in range(len(toPrint)):
                st.markdown("*" + " " + toPrint[i])
            canadian_keycaps.to_csv("csv_files/canadian_keycaps.csv")

if app_mode == "View Dataset":
    st.title("Dataset: canadian_keycaps.csv")
    st.markdown("Dataset :")
    data = pd.read_csv('csv_files/canadian_keycaps.csv')
    data = data[['name', 'vendor', 'price', 'type', 'store']]
    st.write(data)
    clear_button = st.button("Clear data")
    if clear_button:
        canadian_keycaps = pd.DataFrame(columns=["name", "vendor", "price", "type", "store"])
        canadian_keycaps.to_csv("csv_files/canadian_keycaps.csv")

    st.title("Additional info:")
    avg_button = st.button("Average price by store and vendor")
    vendor_count_button = st.button("Number of keycaps by vendor")
    store_count_button = st.button("Number of keycaps by store")
    if avg_button:
        with st.spinner("Loading..."):
            no_names = data[["vendor", "price", "type", "store"]]
            averages = no_names.groupby(["vendor", "store"])["price"].mean()
            averages = averages.to_frame()
            averages.reset_index(inplace=True)
            averages['price'] = round(averages['price'], 2)
            avg_plot = (ggplot(averages, aes(x="store", y="price", fill="vendor"))
                        + geom_col()
                        + ggtitle("Average price by store and vendor")
                        + labs(x="Store", y="Average price (CAD $)", fill="Vendor")
                        )
            avg_plot.save(filename="images/avg_plot.png", height=5, width=5, units='in', dpi=500)
            avg_image = Image.open("images/avg_plot.png")
            st.image(avg_image)
    if vendor_count_button:
        with st.spinner("Loading..."):
            count = data['vendor'].value_counts()
            count = count.to_frame()
            count.reset_index(inplace=True)
            st.write(count)
            vendor_plot = (ggplot(count, aes(x="vendor", y="count", fill="vendor"))
                           + geom_col()
                           + ggtitle("Number of keycaps by vendor")
                           + labs(x="Vendor", y="Count", fill="Vendor")
                           )
            vendor_plot.save(filename="images/vendor_plot.png", height=5, width=5, units='in', dpi=500)
            vendor_image = Image.open("images/vendor_plot.png")
            st.image(vendor_image)
    if store_count_button:
        with st.spinner("Loading..."):
            count = data['store'].value_counts()
            count = count.to_frame()
            count.reset_index(inplace=True)
            st.write(count)
            store_plot = (ggplot(count, aes(x="store", y="count", fill="store"))
                          + geom_col()
                          + ggtitle("Number of keycaps by store")
                          + labs(x="Store", y="Count", fill="Store")
                          )
            store_plot.save(filename="images/store_plot.png", height=5, width=5, units='in', dpi=500)
            store_image = Image.open("images/store_plot.png")
            st.image(store_image)
