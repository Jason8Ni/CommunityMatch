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

def buildMap(location, latitude, longitude):
    mapOfToronto = folium.Map(location=[latitude, longitude], zoom_start=11)

    # add markers to map
    for lat, lng, borough, Neighhbourhood in zip(TorontoPostalData['Latitude'], TorontoPostalData['Longitude'], TorontoPostalData['Borough'], TorontoPostalData['Neighbourhood']):
        label = '{}, {}'.format(Neighhbourhood, borough)
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
    nearbyVenues.columns = ['Neighhbourhood', 
                  'Neighhbourhood Latitude', 
                  'Neighhbourhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearbyVenues)

def getTorontoCoords():
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    latitude = location.latitude
    longitude = location.longitude
    return location, latitude, longitude

TorontoPostalData=pd.read_csv("TorontoPostalData.csv").set_index("PostalCode")

TorontoPostalDataWithCoords = pd.read_csv("TorontoPostalDataWithCoords").set_index("PostalCode")

#foursquare creds

CLIENT_ID = 'INSERT HERE' 
CLIENT_SECRET = 'INSERT HERE'
VERSION = '20180604'
LIMIT = 30
radius = 500

address = 'Toronto'

location, longitude, latitude = getTorontoCoords()
mapOfToronto = buildMap(location, latitude, longitude)

url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    latitude, 
    longitude, 
    radius, 
    LIMIT)

torontoVenues = getNearbyVenues(names=TorontoPostalData['Neighbourhood'],
                                   latitudes=TorontoPostalData['Latitude'],
                                   longitudes=TorontoPostalData['Longitude']
                                  )


TorontoPostalData = TorontoPostalData.reset_index()


torontoVenuesOnehot = pd.get_dummies(torontoVenues[['Venue Category']], prefix="", prefix_sep="")

# add Neighhbourhood column back to dataframe
torontoVenuesOnehot['Neighhbourhood'] = torontoVenues['Neighhbourhood'] 

# move Neighhbourhood column to the first column
fixed_columns = [torontoVenuesOnehot.columns[-1]] + list(torontoVenuesOnehot.columns[:-1])
torontoVenuesOnehot =torontoVenuesOnehot[fixed_columns]

torontoGrouped = torontoVenuesOnehot.groupby('Neighhbourhood').mean().reset_index()
torontoGrouped

#Calc five top venues for each for each neighbourhood

num_top_venues = 5

for hood in torontoGrouped['Neighhbourhood']:
    print("----"+hood+"----")
    temp = torontoGrouped[torontoGrouped['Neighhbourhood'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')

def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]

num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighhbourhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
Neighhbourhoods_venues_sorted = pd.DataFrame(columns=columns)
Neighhbourhoods_venues_sorted['Neighhbourhood'] = torontoGrouped['Neighhbourhood']

for ind in np.arange(torontoGrouped.shape[0]):
    Neighhbourhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(torontoGrouped.iloc[ind, :], num_top_venues)

TorontoPostalData.columns=["PostalCode", "Neighhbourhood", "Borough", "Latitude", "Longitude"]

TorontoPostalData = TorontoPostalData.reset_index()

# CLUSTERING 
# set number of clusters
kclusters = 3

torontoClustering = torontoGrouped.drop('Neighhbourhood', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(torontoClustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 

torontoAllData = TorontoPostalData

# merge toronto_grouped with toronto_data to add latitude/longitude for each Neighhbourhood
torontoAllData = torontoAllData.join(Neighhbourhoods_venues_sorted.set_index('Neighhbourhood'), on='Neighhbourhood')

torontoAllData = torontoAllData.dropna(axis = 0).reset_index(drop=True)

torontoAllData['Cluster Labels'] = kmeans.labels_

# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(torontoAllData['Latitude'], torontoAllData['Longitude'], torontoAllData['Neighhbourhood'], torontoAllData['Cluster Labels']):
    label = folium.Popup(str(poi) + ' Cluster ' + str(cluster), parse_html=True)
    folium.CircleMarker(
        [lat, lon],
        radius=5,
        popup=label,
        color=rainbow[cluster-1],
        fill=True,
        fill_color=rainbow[cluster-1],
        fill_opacity=0.7).add_to(map_clusters)
       
map_clusters

