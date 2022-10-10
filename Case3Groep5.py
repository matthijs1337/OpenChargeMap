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
combo_list.append(Provincie("Zuid-Holland", 51.9862, 4.467313))
combo_list.append(Provincie("Zeeland", 51.9862, 4.467313))
combo_list.append(Provincie("Noord-Brabant", 51.9862, 4.467313))
combo_list.append(Provincie("Flevoland", 51.9862, 4.467313))
combo_list.append(Provincie("Overijssel", 51.9862, 4.467313))
combo_list.append(Provincie("Limburg", 51.9862, 4.467313))
combo_list.append(Provincie("Drenthe", 51.9862, 4.467313))
combo_list.append(Provincie("Groningen", 51.9862, 4.467313))
combo_list.append(Provincie("Friesland", 51.9862, 4.467313))
combo_list.append(Provincie("Gelderland", 51.9862, 4.467313))
combo_list.append(Provincie("Utrecht", 51.9862, 4.467313))

for obj in combo_list:
  original_list.append(obj.provincie)

result = st.selectbox('Selecteer de provincie', original_list)
st.write(f'De gekozen plek {result}')

for obj in combo_list:
   if (result == obj.provincie):
      querystring = {"lat": obj.latitude,"lon":obj.longitude, "output": "json", "compact": True, "verbose": False}

st.write(f'{querystring}')

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)
tekst = response.json()

df = pd.DataFrame.from_dict(tekst)
