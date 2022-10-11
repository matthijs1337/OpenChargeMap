# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 19:02:30 2022

@author: matth
"""


import pandas as pd
import requests
import streamlit as st

class Provincie:
  def __init__ (self, provincie, longitude, latitude):
    self.provincie = provincie
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.provincie, self.longitude, self.latitude)

url = "https://api.openchargemap.io/v3/poi"


headers = {"Content-Type": "application/json", "X-API-Key": "fa5db543-c4ac-4809-8455-9a20a41a021e"}



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
      querystring = {"latitude": obj.latitude,"longitude":obj.longitude, "output": "json", "compact": True, "verbose": False}



###### response

st.write(f'{querystring}')

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)
tekst = response.json()
Open_Charge_Map=pd.DataFrame(tekst)
st.title("Hoi")
st.dataframe(Open_Charge_Map)

### data cleaning
api_data = Open_Charge_Map

dfadress = pd.DataFrame(api_data['AddressInfo'].values.tolist())
dfadress

api_data.drop(['AddressInfo'], axis=1)

mergedDf = dfadress.merge(api_data, how='right', left_index=True, right_index=True)
mergedDf

 api_clean= mergedDf[['ID_y', 'NumberOfPoints',
       'DateCreated', 'UsageCost', 'ID_x', 'Title', 'AddressLine1', 'Town', 'Postcode', 'CountryID',
       'Latitude', 'Longitude'
       ]]
api_clean

api_clean.rename(columns={'ID_y': 'ID', 'ID_x': 'Adress_ID', 'AddressLine1' : 'Adress'})

