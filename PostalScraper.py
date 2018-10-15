
# coding: utf-8

# In[9]:


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import urllib2.open


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


# In[35]:


for cell in row.find_all('th'):
    print(cell.text)

