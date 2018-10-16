
# coding: utf-8

# In[158]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


# In[159]:


postalData = pd.DataFrame(columns = ["PostalCode", "Borough", "Neighbourhood"])


# In[160]:


obj  = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")

page = obj.text

soup = BeautifulSoup(page, "lxml")


# In[161]:


print(soup)


# In[162]:


dataTable = soup.find('table', class_='wikitable sortable')


# In[163]:


row = dataTable.find('tr')


# In[164]:


print(row)


# In[165]:


rowData = row.find_all('th')


# In[166]:


print(rowData)


# In[167]:


print(dataTable.find_all('tr'))


# In[168]:




for row in dataTable.find_all('tr')[1:]:
    temp = []
    for cell in row.find_all('td'):
        temp.append(cell.text)
        #print(cell.text)
    print(temp)
    postalData = postalData.append(
    dict(zip(["PostalCode", "Borough", "Neighbourhood"], temp)), ignore_index=True)


# In[169]:


postalData = postalData[postalData.Borough != "Not assigned"]
postalData["Neighbourhood"] = postalData["Neighbourhood"].replace({'\n':''}, regex=True)
postalData=postalData.reset_index()


# In[173]:


print(postalData)


# In[175]:


postalData = postalData.drop(["index"], axis = 1)


# In[176]:


print(postalData)


# In[177]:


postalData.set_value(6,'Neighbourhood', "Queen's Park")


# In[178]:


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


# In[180]:


postDataFiltered = postalData.groupby(["PostalCode"]).agg({"Borough": lambda x: select_Borough(x),
                                 "Neighbourhood": lambda x: concatenate_neighbourhood(x)})
postDataFiltered.head()


# In[182]:


postDataFiltered


# In[183]:


postDataFiltered.shape

