# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:53:51 2022

@author: matth
"""



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




        url = "https://api.openchargemap.io/v3/poi/?maxresults=7900"
        params = {"latitude": 52.377956, "longitude": 4.897070, "countrycode": "NL","output": "json", "compact": True, "verbose": False}
        headers = {"Content-Type": "application/json", "X-API-Key": "2401ef11-fde1-4b32-a14f-16f0244ddd38"}
        response = requests.request("GET", url, headers=headers, params=params)
        
        json=response.json()
        Open_Charge_Map=pd.DataFrame(json)
        api_data=Open_Charge_Map
        
        dfadress = pd.DataFrame(api_data['AddressInfo'].values.tolist())
        
        api_data.drop(['AddressInfo'], axis=1)
        mergedDf = dfadress.merge(api_data, how='right', left_index=True, right_index=True)
        
        api_clean= mergedDf[['ID_y', 'NumberOfPoints',
           'DateCreated', 'UsageCost', 'ID_x', 'Title', 'AddressLine1', 'Town', 'Postcode', 'CountryID',
           'Latitude', 'Longitude'
           ]]
        
        api_clean.rename(columns={'ID_y': 'ID', 'ID_x': 'Adress_ID', 'AddressLine1' : 'Adress'})
        
        #dropdownlijst
        combo_list=[]
        original_list = []
        combo_list.append(Provincie("Alles", 52.377956, 4.897070))
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
           
        for obj in combo_list:
            if (result == obj.provincie):
              querystring = [obj.latitude, obj.longitude]
        
         #importeren
        postcode_provincie = pd.read_excel('postcode_provincie.xls',index_col=None)
        
        #opsplitsen
        postcode_provincie['list'] = postcode_provincie.apply(lambda x: opsplitsen_postcode(x['aanelkaar']), axis = 1)
        df_data = pd.DataFrame(postcode_provincie['list'].values.tolist(), index=postcode_provincie.index)
        postcode_provincie = pd.concat([postcode_provincie, df_data], axis=1).drop('list', axis=1)
        postcode_provincie.columns = ['orgineel', "begin", 'einde', 'provincie']
        postcode_provincie.head()
        
        #missende postcodes toevoegen
        postcode = []
        provincie = []
        
        row = 0
        for i, row in postcode_provincie.iterrows():
            lijst = (row.einde - row.begin+1)* [row.provincie]
            lijst2 = [*range(row.begin, row.einde+1)]
            provincie += lijst
            postcode += lijst2
        
        dict2 = {'Postcode_cijfer': postcode, 'Provincie': provincie}  
        postcode_split = pd.DataFrame(dict2)
        
        api_clean['Postcode_cijfer'] = api_clean.Postcode.apply(postcode_nummers)
        Provinice_df = api_clean.merge(postcode_split,how="left",left_on="Postcode_cijfer",right_on="Postcode_cijfer")

        
        if result == "Alles":
            api_provincie = Provinice_df
            a = folium.Map(location=querystring, zoom_start=7)
        else:
            api_provincie = Provinice_df[Provinice_df['Provincie'] == result]
            a = folium.Map(location=querystring, zoom_start=8.5)
        
        
        ######### foliummap
        logo_url = 'https://www.laadpalenwijzer.nl/wp-content/uploads/2022/03/laadpaal-icon-by-monkik.png'
        
        
        marker_cluster2 = MarkerCluster().add_to(a)
        
        
        for i, x in api_provincie.iterrows():
            folium.Marker(location=[x['Latitude'], x['Longitude']],
                               popup="<strong>" + x['Title'] +"<strong>",
                               tooltip='Klik hier om het adres te zien',
                               fill_opacity=0.7,
                               fill= True,
                               icon= folium.features.CustomIcon(logo_url,\
                                          icon_size=(50, 50))
                               ).add_to(marker_cluster2)
        
        st_data = st_folium(a, width = 725)
