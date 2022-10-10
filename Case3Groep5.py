# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:59:05 2022

@author: matth
"""
#Streamlit link: https://matthijs1337-openchargemap-case3groep5-j60f5d.streamlitapp.com/
import pandas as pd
import requests
import json
import streamlit as st
import plotly.graph_objects as go
#import plotly.express as px

import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years

import plotly.io as pio
pio.renderers.default = 'browser'

#class provincie
class Provincie: 
   def __init__ (self, provincie, latitude, longitude): 
     self.provincie = provincie
     self.longitude = longitude
     self.latitude = latitude
     def show_all(self): 
         print (self.provincie, self.latitude, self.longitude)


url = "https://api.openchargemap.io/v3/poi"

#params = {"latitude": 52.0907374, "longitude": -5.1214201, "countrycode": "NL", 

#params2= {"output": "json", "compact": True, "verbose": False}

headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}


combo_list=[]
original_list = []
combo_list.append(Provincie("Noord-Holland", 52.3750294, 4.6309628))

for obj in original_list:
   original_list.append(obj.provincie) 
  
#radio 
result = st.sidebar.selectbox('Selecteer een Provincie', original_list)
  
for obj in combo_list: 
   if (result == obj.provincie):
        querystring = {"lat":obj.latitude, 'lng':obj.longitude, "output": "json", "compact": True, "verbose": False}
        
response = requests.get(url, headers=headers, params=querystring)
a=response.json()
Open_Charge_Map=pd.DataFrame(a)
st.title("Hoi")
st.dataframe(Open_Charge_Map)
