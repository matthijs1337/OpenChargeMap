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

params = {"latitude": 52.0907374, "longitude": -5.1214201, "countrycode": "NL", 

"output": "json", "compact": True, "verbose": False}

headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}

response = requests.request("GET", url, headers=headers, params=params)

json=response.json()
Open_Charge_Map=pd.DataFrame(json)
Open_Charge_Map.head()
