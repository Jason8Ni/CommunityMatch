
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


# In[4]:


postalData = pd.DataFrame(columns = ["PostalCode", "Borough", "Neighbourhood"])


# In[5]:


obj  = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")

page = obj.text

soup = BeautifulSoup(page, "lxml")


# In[6]:


print(soup)


# In[7]:


dataTable = soup.find('table', class_='wikitable sortable')


# In[8]:


row = dataTable.find('tr')


# In[9]:


print(row)


# In[10]:


rowData = row.find_all('th')


# In[11]:


print(rowData)


# In[12]:


print(dataTable.find_all('tr'))


# In[13]:




for row in dataTable.find_all('tr')[1:]:
    temp = []
    for cell in row.find_all('td'):
        temp.append(cell.text)
        #print(cell.text)
    print(temp)
    postalData = postalData.append(
    dict(zip(["PostalCode", "Borough", "Neighbourhood"], temp)), ignore_index=True)


# In[14]:


postalData = postalData[postalData.Borough != "Not assigned"]
postalData["Neighbourhood"] = postalData["Neighbourhood"].replace({'\n':''}, regex=True)
postalData=postalData.reset_index()


# In[15]:


print(postalData)


# In[16]:


postalData = postalData.drop(["index"], axis = 1)


# In[17]:


print(postalData)


# In[18]:


postalData.set_value(6,'Neighbourhood', "Queen's Park")


# In[19]:


def concatenate_neighbourhood(x):
    cadena = ""
    for i in range(len(x)-1):
        cadena = cadena + x.iloc[i] + ", "
    cadena += x.iloc[-1]
    return cadena

def select_Borough(x):
    ref = x.iloc[0]
    for i in range(1, len(x)):
        if ref != x.iloc[i]:
            for i in x:
                print(x)
            raise Exception("Postcode comprises two Boroughs")
    return ref


# In[20]:


postDataFiltered = postalData.groupby(["PostalCode"]).agg({"Borough": lambda x: select_Borough(x),
                                 "Neighbourhood": lambda x: concatenate_neighbourhood(x)})
postDataFiltered.head()


# In[21]:


postDataFiltered


# In[22]:


postDataFiltered = postDataFiltered.reset_index()
postDataFiltered


# In[23]:


import sys
get_ipython().system(u'{sys.executable} -m pip install geocoder')


# In[24]:


print(postDataFiltered.head())


# In[25]:


import geocoder


# In[ ]:


latitude = []
longitude = []


#print(postDataFiltered)
# loop until you get the coordinates
for index, row in postDataFiltered.iterrows():
    postal_code = row.PostalCode
    lat_lng_coords = None
    while(lat_lng_coords is None):
        g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
        lat_lng_coords = g.latlng
        print(lat_lng_coords)
    latitude.append(lat_lng_coords[0])
    longitude.append(lat_lng_coords[1])


# In[ ]:


print(latitude)
print(longitude)


# In[28]:


postDataFiltered.to_csv("TorontoPostalData.csv")


# In[34]:


import pandas as pd
Toronto_data = pd.read_csv("TorontoPostalData.csv").set_index("PostalCode")
Toronto_data.head()
Toronto_data = Toronto_data.drop(["Unnamed: 0"], axis = 1)
Toronto_data.head()


# In[37]:


LatLongData = pd.read_csv("http://cocl.us/Geospatial_data").set_index("Postal Code")


# In[39]:


LatLongData.head()
TorontoPostalData = Toronto_data.join(LatLongData)


# In[40]:


TorontoPostalData.head()


# In[43]:


from IPython.display import HTML
import base64

def create_download_link( df, title = "Download CSV file", filename = "data.csv"):  
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload,title=title,filename=filename)
    return HTML(html)

create_download_link(TorontoPostalData)


# In[44]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system(u"conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab")
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system(u"conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library

print('Libraries imported.')
TorontoPostalData


# In[61]:


CLIENT_ID = 'JWI5QI3OKOZ0B2LTI11AZYGAA1JWVYTGY5WGITUI1CDOPFXY' 
CLIENT_SECRET = 'JXSBJ3I24WKHDTU5NOPR1CRC34EGDT5B1FWXAVOTUDUD5E2M'
VERSION = '20180604'
LIMIT = 100
radius = 500


# In[48]:


address = 'Toronto'

geolocator = Nominatim()
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The geograpical coordinate of Toronto are {}, {}.'.format(latitude, longitude))


# In[54]:



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
    
mapOfToronto


# In[56]:


TorontoPostalData = TorontoPostalData.reset_index()


# In[58]:


TorontoPostalData.loc[0, 'Neighbourhood']


# In[62]:


url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&ll={},{}&radius={}&limit={}'.format(
    CLIENT_ID, 
    CLIENT_SECRET, 
    VERSION, 
    latitude, 
    longitude, 
    radius, 
    LIMIT)


# In[63]:


results = requests.get(url).json()
results


# In[64]:


def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# In[65]:


venues = results['response']['groups'][0]['items']
    
nearby_venues = json_normalize(venues) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories', 'venue.location.lat', 'venue.location.lng']
nearby_venues =nearby_venues.loc[:, filtered_columns]

# filter the category for each row
nearby_venues['venue.categories'] = nearby_venues.apply(get_category_type, axis=1)

# clean columns
nearby_venues.columns = [col.split(".")[-1] for col in nearby_venues.columns]

nearby_venues.head()


# In[67]:


def getNearbyVenues(names, latitudes, longitudes, radius=500):
    
    venues_list=[]
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
        venues_list.append([(
            name, 
            lat, 
            lng, 
            v['venue']['name'], 
            v['venue']['location']['lat'], 
            v['venue']['location']['lng'],  
            v['venue']['categories'][0]['name']) for v in results])

    nearby_venues = pd.DataFrame([item for venue_list in venues_list for item in venue_list])
    nearby_venues.columns = ['Neighborhood', 
                  'Neighborhood Latitude', 
                  'Neighborhood Longitude', 
                  'Venue', 
                  'Venue Latitude', 
                  'Venue Longitude', 
                  'Venue Category']
    
    return(nearby_venues)


# In[68]:


torontoVenues = getNearbyVenues(names=TorontoPostalData['Neighbourhood'],
                                   latitudes=TorontoPostalData['Latitude'],
                                   longitudes=TorontoPostalData['Longitude']
                                  )


# In[85]:


torontoVenues.shape


# In[70]:


torontoVenues.head()


# In[74]:


# one hot encoding
torontoVenuesOnehot = pd.get_dummies(torontoVenues[['Venue Category']], prefix="", prefix_sep="")

# add neighborhood column back to dataframe
torontoVenuesOnehot['Neighborhood'] = torontoVenues['Neighborhood'] 

# move neighborhood column to the first column
fixed_columns = [torontoVenuesOnehot.columns[-1]] + list(torontoVenuesOnehot.columns[:-1])
torontoVenuesOnehot =torontoVenuesOnehot[fixed_columns]

torontoVenuesOnehot.head()


# In[77]:


torontoGrouped = torontoVenuesOnehot.groupby('Neighborhood').mean().reset_index()
torontoGrouped


# In[78]:


torontoGrouped.shape


# In[79]:


#Calc five top venues for each for each neighbourhood

num_top_venues = 5

for hood in torontoGrouped['Neighborhood']:
    print("----"+hood+"----")
    temp = torontoGrouped[torontoGrouped['Neighborhood'] == hood].T.reset_index()
    temp.columns = ['venue','freq']
    temp = temp.iloc[1:]
    temp['freq'] = temp['freq'].astype(float)
    temp = temp.round({'freq': 2})
    print(temp.sort_values('freq', ascending=False).reset_index(drop=True).head(num_top_venues))
    print('\n')


# In[80]:


def return_most_common_venues(row, num_top_venues):
    row_categories = row.iloc[1:]
    row_categories_sorted = row_categories.sort_values(ascending=False)
    
    return row_categories_sorted.index.values[0:num_top_venues]

num_top_venues = 10

indicators = ['st', 'nd', 'rd']

# create columns according to number of top venues
columns = ['Neighborhood']
for ind in np.arange(num_top_venues):
    try:
        columns.append('{}{} Most Common Venue'.format(ind+1, indicators[ind]))
    except:
        columns.append('{}th Most Common Venue'.format(ind+1))

# create a new dataframe
neighborhoods_venues_sorted = pd.DataFrame(columns=columns)
neighborhoods_venues_sorted['Neighborhood'] = torontoGrouped['Neighborhood']

for ind in np.arange(torontoGrouped.shape[0]):
    neighborhoods_venues_sorted.iloc[ind, 1:] = return_most_common_venues(torontoGrouped.iloc[ind, :], num_top_venues)

neighborhoods_venues_sorted


# In[97]:


print(torontoClustering.shape)
TorontoPostalData.head()
TorontoPostalData.columns=["PostalCode", "Neighborhood", "Borough", "Latitude", "Longitude"]


# In[101]:


TorontoPostalData = TorontoPostalData.reset_index()
TorontoPostalData.head()


# In[119]:


# set number of clusters
kclusters = 3

torontoClustering = torontoGrouped.drop('Neighborhood', 1)

# run k-means clustering
kmeans = KMeans(n_clusters=kclusters, random_state=0).fit(torontoClustering)

# check cluster labels generated for each row in the dataframe
kmeans.labels_[0:10] 

torontoAllData = TorontoPostalData

# merge toronto_grouped with toronto_data to add latitude/longitude for each neighborhood
torontoAllData = torontoAllData.join(neighborhoods_venues_sorted.set_index('Neighborhood'), on='Neighborhood')

torontoAllData.head() # check the last columns!


# In[120]:


torontoAllData = torontoAllData.dropna(axis = 0).reset_index(drop=True)


# In[121]:


torontoAllData['Cluster Labels'] = kmeans.labels_


# In[122]:


torontoAllData


# In[123]:


# create map
map_clusters = folium.Map(location=[latitude, longitude], zoom_start=11)

# set color scheme for the clusters
x = np.arange(kclusters)
ys = [i+x+(i*x)**2 for i in range(kclusters)]
colors_array = cm.rainbow(np.linspace(0, 1, len(ys)))
rainbow = [colors.rgb2hex(i) for i in colors_array]

# add markers to the map
markers_colors = []
for lat, lon, poi, cluster in zip(torontoAllData['Latitude'], torontoAllData['Longitude'], torontoAllData['Neighborhood'], torontoAllData['Cluster Labels']):
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

