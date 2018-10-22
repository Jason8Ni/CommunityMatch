# CommunityMatch

## Toronto Neighbourhood Clustering and Analysis

### Process

The area codes in the GTA were scraped from a Wikipedia article and put in a dataframe. Then, unique values of postal code were found and the encompassing neighbourhoods were grouped. 

Next Geocoder was used to the the positional coordinates (longitude and latitude) of each postal code.

After this was done, and the dataframe was exported to `TorontoPostalData.csv`, further data can be gathered. 

### Data collection

Additional data was collected about each neighbourhood. The idea was to cluster and determine similar neighbourhoods across Toronto based on the types of venues that they offered. To gather this data, the Foursquare API was used. This API provides real-time geographical data of almost anywhere on Earth. 


## Training

Training was done using scikit-learn. Any other external library like Tensorflow was throught to be overkill for this exploratory problem. 

A simple K-Means algorithm was used. 
## Data visualization

Maps were built and created using Folium.

Neighbourhoods of Toronto: 

![](https://github.com/Jason8Ni/CommunityMatch/blob/master/toronto.PNG)

Toronto Neighbourhoods labelled 3 clusters:

![](https://github.com/Jason8Ni/CommunityMatch/blob/master/3cluster.PNG)

Toronto Neighbourhoods labelled with 5 clusters:

![](https://github.com/Jason8Ni/CommunityMatch/blob/master/5cluster.PNG)

Toronto Neighbourhoods labelled with 10 clusters:

![](https://github.com/Jason8Ni/CommunityMatch/blob/master/10Cluster.PNG)

## TODO

* Build something cool out of the trainer
* Something that predicts/recommends a neighbourhood to you? 
    * Build some kind of recommender system
* Build a web application to support this
* Further complexity of cluster to look for other trends in data
