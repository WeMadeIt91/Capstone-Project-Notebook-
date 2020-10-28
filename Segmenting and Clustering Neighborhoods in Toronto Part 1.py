#!/usr/bin/env python
# coding: utf-8

# # installing/importing necessary libraries for assignment

# In[ ]:


pip install geopy


# In[ ]:


get_ipython().system('pip install lxml')


# In[1]:


import lxml
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import matplotlib.cm as cm
import matplotlib.colors as colors
from sklearn.cluster import KMeans

import json
from geopy.geocoders import Nominatim 


# # Download & Explore Data Set into a Pandas Dataframe

# In[2]:


read= 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
ds = pd.read_html(read, index_col=[0])
Ctable = ds[0]
Ctable


# # processes the cells that have an assigned borough. Ignore cells with a borough that is Not assigned. This shows how many rows have a not assigned value.

# In[3]:


Ctable.Borough.value_counts()


# # replaces 'Not assigned' with another value

# In[4]:


Ctable.Borough.replace("Not assigned", np.nan, inplace = True) 
Ctable.head()


# In[5]:


Ctable.Borough.value_counts #shows not assigned replaced with NaN


# # drops nan from the table

# In[11]:


Ctable.dropna(axis=0, inplace=True)
Ctable = Ctable.reset_index()
Ctable = Ctable.drop(['index'], axis=1)
Ctable.head(20)


# # Deletes the first column called level_0

# In[12]:


del Ctable['level_0']


# In[13]:


Ctable


# # look at the first 12 rows

# In[14]:


Ctable.head(12)


# # This is where the selections are grouped by postal code, borough and neighborhood

# In[15]:


Ctable = Ctable.groupby(['Postal Code', 'Borough'])['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
Ctable = Ctable.reset_index()
Ctable.head(50)


# # Obtaining the shape of the table: columns and rows

# In[16]:


Ctable.shape


# # Read in the second file

# In[37]:


read2 = 'http://cocl.us/Geospatial_data'
Geof = pd.read_csv(read2, index_col=[0])
Geof


# # Merge first dataframe with newly read dataframe

# In[45]:


GeoTable=pd.merge(Ctable,Geof, on='Postal Code')
GeoTable


# # Install and import folium for map visualization

# In[50]:


pip install folium


# In[51]:


import folium


# # determine Toronto, Canada's coordinates

# In[55]:


Add = 'Toronto, Canada'
geoL = Nominatim(user_agent="to_explorer")
location = geoL.geocode(Add)
Lat = location.latitude
Long = location.longitude
print('The geograpical coordinates of Toronto, Canada are the following: {}, {}.'.format(Lat, Long))


# # Visualize Toronto with folium maps

# In[92]:


Tmap = folium.Map(location=[43.6534817, -79.3839347], tiles='stamenterrain', zoom_start=12)
print("This is a map of Toronto and surrounding areas ")
Tmap


# # Adding labels and markers to Toronto Map

# In[98]:


for lat, lng, borough, neighborhood in zip(GeoTable['Latitude'], GeoTable['Longitude'], GeoTable['Borough'], GeoTable['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=7,
        popup=label,
        color='purple',
        fill=True,
        fill_color='#232c43',
        fill_opacity=0.7,
        parse_html=False).add_to(Tmap) 
print(Tmap)


# In[101]:





# In[ ]:




