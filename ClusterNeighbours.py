import numpy as np 

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim 

import matplotlib.cm as cm
import matplotlib.colors as colors

from sklearn.cluster import KMeans

#conda install -c conda-forge folium=0.5.0 --yes 
import folium 

TorontoPostalData=pd.read_csv("TorontoPostalData.csv").set_index("PostalCode")

TorontoPostalDataWithCoords = pd.read_csv("TorontoPostalDataWithCoords").set_index("PostalCode")

#foursquare creds

CLIENT_ID = 'INSERT HERE' 
CLIENT_SECRET = 'INSERT HERE'
VERSION = '20180604'
LIMIT = 30

address = 'Toronto'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))

def buildMap(location, latitude, longitude):
    mapOfToronto = folium.Map(location=[latitude, longitude], zoom_start=11)

    # add markers to map
    for lat, lng, borough, neighborhood in zip(TorontoPostalData['Latitude'], TorontoPostalData['Longitude'], TorontoPostalData['Borough'], TorontoPostalData['Neighbourhood']):
        label = '{}, {}'.format(neighborhood, borough)
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(mapOfToronto)
    return mapOfToronto

mapOfToronto = buildMap(location, latitude, longitude)
