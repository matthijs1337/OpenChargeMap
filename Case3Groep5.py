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

#klas
class Provincie:
  def __init__ (self, provincie, longitude, latitude):
    self.provincie = provincie
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.provincie, self.longitude, self.latitude)

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
#api_data


# In[4]:

dfadress = pd.DataFrame(api_data['AddressInfo'].values.tolist())
#dfadress


# In[5]:


api_data.drop(['AddressInfo'], axis=1)

mergedDf = dfadress.merge(api_data, how='right', left_index=True, right_index=True)
#mergedDf


# In[6]:


api_clean= mergedDf[['ID_y', 'NumberOfPoints',
       'DateCreated', 'UsageCost', 'ID_x', 'Title', 'AddressLine1', 'Town', 'Postcode', 'CountryID',
       'Latitude', 'Longitude'
       ]]
#api_clean


# In[7]:


api_clean.rename(columns={'ID_y': 'ID', 'ID_x': 'Adress_ID', 'AddressLine1' : 'Adress'})


# In[14]:
#dropdownlijst
combo_list=[]
original_list = []
combo_list.append(Provincie("Noord-Holland", 52.375029, 4.630962))
combo_list.append(Provincie("Zuid-Holland", 52.090737, 5.121420))
combo_list.append(Provincie("Zeeland", 51.494030, 3.849681))
combo_list.append(Provincie("Noord-Brabant", 51.4826537, 5.232168))
combo_list.append(Provincie("Flevoland", 52.527978, 5.595350))
combo_list.append(Provincie("Overijssel", 52.438781, 6.501641))
combo_list.append(Provincie("Limburg", 51.442723, 6.060872))
combo_list.append(Provincie("Drenthe", 52.947601, 6.623058))
combo_list.append(Provincie("Groningen", 53.220028, 6.570447))
combo_list.append(Provincie("Friesland", 53.164164, 5.781754))
combo_list.append(Provincie("Gelderland", 52.04515, 5.871823))
combo_list.append(Provincie("Utrecht",52.1195, 5.1944))
    
for obj in combo_list:
    original_list.append(obj.provincie)
    
result = st.selectbox('Selecteer de provincie', original_list)
st.write(f'De gekozen provincie {result}')
   
for obj in combo_list:
    if (result == obj.provincie):
      querystring = [obj.longitude, obj.latitude]
      
st.write(f'QueryString {querystring}')

#locationx=[53,4]
#m = folium.Map(location=querystring, zoom_start=8)

#marker_cluster = MarkerCluster().add_to(m)

#for i, x in api_clean.iterrows():
    #folium.Marker(location=[x['Latitude'], x['Longitude']],
                        #popup="<strong>" + x['Title'] +"<strong>",
                        #tooltip='Klik hier om het adres te zien',
                        #fill_opacity=0.7,
                        #fill= True
                        #).add_to(marker_cluster)

#st_data = st_folium(m, width = 725)

#########tweede foliummap
logo_url = 'https://www.laadpalenwijzer.nl/wp-content/uploads/2022/03/laadpaal-icon-by-monkik.png'

a = folium.Map(location=querystring, zoom_start=7)

marker_cluster2 = MarkerCluster().add_to(a)

for i, x in api_clean.iterrows():
    folium.Marker(location=[x['Latitude'], x['Longitude']],
                       popup="<strong>" + x['Title'] +"<strong>",
                       tooltip='Klik hier om het adres te zien',
                       fill_opacity=0.7,
                       fill= True,
                       icon= folium.features.CustomIcon(logo_url,\
                                  icon_size=(50, 50))
                       ).add_to(marker_cluster2)

st_data = st_folium(a, width = 725)


       


