
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib2.open


# In[41]:


postalData = pd.DataFrame(columns = ["PostalCode", "Borough", "Neighbourhood"])


# In[19]:


obj  = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")

page = obj.text

soup = BeautifulSoup(page, "lxml")


# In[17]:


print(soup)


# In[23]:


dataTable = soup.find('table', class_='wikitable sortable')


# In[25]:


row = dataTable.find('tr')


# In[31]:


print(row)


# In[29]:


rowData = row.find_all('th')


# In[30]:


print(rowData)


# In[55]:




for row in dataTable.find_all('tr'):
    temp = []
    for cell in row.find_all('td'):
        temp.append(cell.text)
        #print(cell.text)
        print(temp)
    postalData = postalData.append(pd.DataFrame(temp).T)
    #print()


# In[53]:


print(postalData)

