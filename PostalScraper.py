import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

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

postalData = pd.DataFrame(columns = ["PostalCode", "Borough", "Neighbourhood"])

obj  = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")

page = obj.text

soup = BeautifulSoup(page, "lxml")

#print(soup)

dataTable = soup.find('table', class_='wikitable sortable')
row = dataTable.find('tr')
rowData = row.find_all('th')

for row in dataTable.find_all('tr')[1:]:
    temp = []
    for cell in row.find_all('td'):
        temp.append(cell.text)
        #print(cell.text)
    print(temp)
    postalData = postalData.append(
    dict(zip(["PostalCode", "Borough", "Neighbourhood"], temp)), ignore_index=True)

postalData = postalData[postalData.Borough != "Not assigned"]
postalData["Neighbourhood"] = postalData["Neighbourhood"].replace({'\n':''}, regex=True)
postalData=postalData.reset_index()
postalData = postalData.drop(["index"], axis = 1)
postalData.set_value(6,'Neighbourhood', "Queen's Park")

postDataFiltered = postalData.groupby(["PostalCode"]).agg({"Borough": lambda x: select_Borough(x),
                                 "Neighbourhood": lambda x: concatenate_neighbourhood(x)})
postDataFiltered.head()
postDataFiltered

postDataFiltered.shape

