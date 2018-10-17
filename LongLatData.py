import pandas as pd

Toronto_data = pd.read_csv("TorontoPostalData.csv").set_index("PostalCode")
Toronto_data.head()
Toronto_data = Toronto_data.drop(["Unnamed: 0"], axis = 1)
#Toronto_data.head()

LatLongData = pd.read_csv("http://cocl.us/Geospatial_data").set_index("Postal Code")

#LatLongData.head()
TorontoPostalData = Toronto_data.join(LatLongData)

TorontoPostalData.to_csv("TorontoPostalDataWithCoords.csv")