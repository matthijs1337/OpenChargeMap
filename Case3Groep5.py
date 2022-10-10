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


headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}



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
combo_list.append(Provincie("Utrecht",52.090737, 5.121420))

for obj in combo_list:
  original_list.append(obj.provincie)

result = st.selectbox('Selecteer de provincie', original_list)
st.write(f'De gekozen plek {result}')

for obj in combo_list:
   if (result == obj.provincie):
      querystring = {"latitude": obj.latitude,"longitude":obj.longitude,  "countrycode": "NL", "output": "json", "compact": True, "verbose": False}

st.write(f'{querystring}')

########################
#url = "https://api.openchargemap.io/v3/poi"

#params = {"latitude": 52.0907374, "longitude": -5.1214201, "countrycode": "NL", "output": "json", "compact": True, "verbose": False}

#headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}

#response = requests.request("GET", url, headers=headers, params=params)


#############################


response = requests.request("GET", url, headers=headers, params=querystring)
st.title("Hoi")
json=response.json()
Open_Charge_Map=pd.DataFrame(json)
st.dataframe(Open_Charge_Map)


