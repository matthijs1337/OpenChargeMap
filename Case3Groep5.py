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

url = "https://api.openchargemap.io/v3/poi"

params = {"latitude": 52.0907374, "longitude": -5.1214201, "countrycode": "NL", 

"output": "json", "compact": True, "verbose": False}

headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}

response = requests.request("GET", url, headers=headers, params=params)

json=response.json()
Open_Charge_Map=pd.DataFrame(json)

st.title("Hoi")
st.dataframe(Open_Charge_Map)

