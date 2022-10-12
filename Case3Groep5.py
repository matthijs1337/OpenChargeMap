# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:53:51 2022

@author: matth
"""
# In[1]:


import pandas as pd
import requests
import json
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import st_folium


# In[2]:


url = "https://api.openchargemap.io/v3/poi/?maxresults=7900"

params = {"latitude": 52.377956, "longitude": 4.897070, "countrycode": "NL", 

"output": "json", "compact": True, "verbose": False}

headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}

response = requests.request("GET", url, headers=headers, params=params)


# In[3]:


json=response.json()
Open_Charge_Map=pd.DataFrame(json)
api_data=Open_Charge_Map
api_data


# In[4]:

dfadress = pd.DataFrame(api_data['AddressInfo'].values.tolist())
dfadress


# In[5]:


api_data.drop(['AddressInfo'], axis=1)

mergedDf = dfadress.merge(api_data, how='right', left_index=True, right_index=True)
mergedDf


# In[6]:


api_clean= mergedDf[['ID_y', 'NumberOfPoints',
       'DateCreated', 'UsageCost', 'ID_x', 'Title', 'AddressLine1', 'Town', 'Postcode', 'CountryID',
       'Latitude', 'Longitude'
       ]]
api_clean


# In[7]:


api_clean.rename(columns={'ID_y': 'ID', 'ID_x': 'Adress_ID', 'AddressLine1' : 'Adress'})


# In[14]:


m = folium.Map(location=[52.377956, 4.897070], zoom_start=7)

#marker_cluster = MarkerCluster().add_to(m)

for i, x in api_clean.iterrows():
    folium.Marker(location=[x['Latitude'], x['Longitude']],
                        popup="<strong>" + x['Title'] +"<strong>",
                        tooltip='Klik hier om het adres te zien',
                        fill_opacity=0.7,
                        fill= True
                        ).add_to(m)

st_data = st_folium(m. width = 725)

