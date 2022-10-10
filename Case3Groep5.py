# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:59:05 2022

@author: matth
"""
#Streamlit link: https://matthijs1337-openchargemap-case3groep5-j60f5d.streamlitapp.com/

import pandas as pd
import requests
import json

url = "https://api.openchargemap.io/v3/poi"

headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}
params = {"countrycode": "NL", "output": "json", "compact": True, "verbose": False}
response = requests.request("GET", url, headers=headers, params=querystring)

json=response.json()
Open_Charge_Map=pd.DataFrame(json)
Open_Charge_Map.head()

#klasse gemeente
class gemeente:
  def __init__ (self, gemeente, latitude, longitude):
    self.gemeente = gemeente
    self.longitude = longitude
    self.latitude = latitude
    def show_all(self):
        print (self.land, self.latitude, self.longitude)
        
        
combo_list=[]
original_list = []
combo_list.append(gemeente("Amsterdam", 52.3667, 4.8945))




for obj in combo_list:
  original_list.append(obj.gemeente)

#radio
result = st.sidebar.selectbox('Select a city', original_list)

for obj in combo_list:
    if (result == obj.gemeente):
      querystring = {"lat": obj.latitude,"lon":obj.longitude}
