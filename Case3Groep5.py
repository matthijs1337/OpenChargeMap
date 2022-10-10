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
    self.land = provincie
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.provincie, self.longitude, self.latitude)

url = "https://api.openchargemap.io/v3/poi"


headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}



combo_list=[]
original_list = []
combo_list.append(Provincie("Noord-Holland", 52.3750294, 4.6309628))

for obj in combo_list:
  original_list.append(obj.Provincie)


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


df_data = pd.DataFrame(df['data'].values.tolist(), index=df.index)
df2 = pd.concat([df, df_data], axis=1).drop('data', axis=1)
df_data = pd.DataFrame(df2['weather'].values.tolist(), index=df.index) 
df2 = pd.concat([df2, df_data], axis=1).drop('weather', axis=1)

st.dataframe(df2)


print(df2.info())
