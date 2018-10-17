import numpy as np 

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim 
import json

import matplotlib.cm as cm
import matplotlib.colors as colors

from sklearn.cluster import KMeans

#conda install -c conda-forge folium=0.5.0 --yes 
import folium 

import requests 
from pandas.io.json import json_normalize 


TorontoPostalData=pd.read_csv("TorontoPostalData.csv").set_index("PostalCode")

TorontoPostalDataWithCoords = pd.read_csv("TorontoPostalDataWithCoords").set_index("PostalCode")

#foursquare creds

CLIENT_ID = 'INSERT HERE' 
CLIENT_SECRET = 'INSERT HERE'
VERSION = '20180604'
LIMIT = 30
radius = 500

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

def getCategoryType(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venuesList=[]
    for name, lat, lng in zip(names, latitudes, longitudes):
        print(name)
            
        # create the API request URL
        url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
            CLIENT_ID, 
            CLIENT_SECRET, 
            VERSION, 
            lat, 
            lng, 
            radius, 
            LIMIT)
            
        # make the GET request
        results = requests.get(url).json()["response"]['groups'][0]['items']
        
        # return only relevant information for each nearby venue
        venuesList.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearbyVenues = pd.DataFrame([item for venue_list in venuesList for item in venue_list])
    nearbyVenues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearbyVenues)

mapOfToronto = buildMap(location, latitude, longitude)

url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    latitude, 
    longitude, 
    radius, 
    LIMIT)


