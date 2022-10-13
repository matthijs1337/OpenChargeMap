# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:53:51 2022

@author: matth
"""

# pip install sodapy

import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import statistics
import json
import folium
from streamlit_folium import st_folium
import xlrd
import plotly.figure_factory as ff


import plotly.io as pio
pio.renderers.default = 'browser'


class Provincie:
  def __init__ (self, provincie, latitude, longitude):
    self.provincie = provincie
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.provincie, self.longitude, self.latitude)


def opsplitsen_postcode(value):
        begin = value[0:4]
    
        if value[5] == '-':
            einde = value[7:11]
            provincie = value[12:]
        else:
            einde = begin
            provincie = value[5:]
    
        #rare waardes eruit halen
        if provincie == 'Utrecht\xa0voorheen\xa0Zuid-Holland':
            provincie = 'Utrecht'
    
    
        return [int(begin), int(einde), provincie] 
    
def postcode_nummers(value):
    value = str(value)
    if len(value) != 0:

        if value[0] == ' ':
            value = value[1:]

        if len(value) >= 4:
            return int(value[0:4])
        else:
            return 9999

st.set_page_config(layout = 'wide')

st.title("Informatie over elektrische  auto's en laadpaal locaties")
tab1, tab2, tab3 = st.tabs(["Laadpaal locaties", "Laadpaal data", "Elektrische auto's"])


#openChargeMap
with tab1: 
    col1b, col2b = st.columns([1, 1])
    
    with col1b:
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

    with col2b:
        st.markdown("**Aantal laadpalen per provincie**")
        aantal = Provinice_df.groupby('Provincie',as_index = False )['Postcode_cijfer'].count()
        aantal.columns = ['Provincie', 'Aantal']
        st.dataframe(aantal)


      



#Laadpaaldata
with tab2:
    col1a, col2a, col3a = st.columns([1, 1, 1])
    
    with col1a:
        st.markdown("**Voorspeling voor de bezetting van de laadpaal**")
        
        laadpaaldata = pd.read_csv("laadpaaldata.csv")
        
        laadpaaldata= laadpaaldata[laadpaaldata["ConnectedTime"]>0]
        laadpaaldata= laadpaaldata[laadpaaldata["ChargeTime"]>0]
        laadpaaldata= laadpaaldata[laadpaaldata["ConnectedTime"]<13]
        laadpaaldata= laadpaaldata[laadpaaldata["ChargeTime"]<3]
        
        laadpaaldata1 = laadpaaldata[laadpaaldata['Started'].str.contains("2018-02-29")==False]
        laadpaaldata1['Started']= pd.to_datetime(laadpaaldata1['Started'],format='%Y-%m-%d %H:%M:%S')
        
        
        df_laadpaal = laadpaaldata1.copy()
        df_laadpaal['maand'] = pd.to_datetime(df_laadpaal['Started']).dt.month
        df_laadpaal['uur'] = pd.to_datetime(df_laadpaal['Started']).dt.hour
        
        
        mdl2 = ols(' ConnectedTime ~ ChargeTime  + uur + MaxPower + TotalEnergy', data = df_laadpaal).fit()
        
        with st.form("my_form"):
            number1 = st.number_input('Oplaad duur in uur', value = 0)
            number2 = st.number_input('Uur van de starttijd (0-23)', value = 0)
            number3 = st.number_input('Maximale laadsnelheid in W', value = 0)
            number4 = st.number_input('Totale verbruikte energy in Wh', value = 0)
        
            # Every form must have a submit button.
            submitted = st.form_submit_button("Bereken bezetting van de laadpaal")
            if submitted:
                
                explanatory_data = pd.DataFrame({'ChargeTime': [number1], 'uur': [number2],'MaxPower': [number3],'TotalEnergy': [number4]})
                result = mdl2.predict(explanatory_data)
                
                st.markdown("**Voorspelde bezetting van de laadpaal**")
                st.markdown(result.iloc[0])
        
        with col2a:
            
            fig2 = px.histogram(laadpaaldata1, x = 'ConnectedTime', 
                            title = 'Histogram van de bezetting van de laadpaal in 2018',
                            color_discrete_sequence = ['rgb(224, 224, 224)'], nbins = 30
                            )
            fig2.update_layout(
                            xaxis=dict(title = 'Bezetting van de paal'),
                            yaxis=dict(title = "Aantal laadsessies"))
            
            fig2.update_traces(marker_line_width=1,marker_line_color="black")
            fig2.add_vline(x=laadpaaldata1['ConnectedTime'].median(),line_dash="dot", line_width=1, line_color="black")
            fig2.add_annotation(x=laadpaaldata1['ConnectedTime'].median()  - 0.7, y=800, text="mediaan", showarrow=False)
            fig2.add_vline(x=laadpaaldata1['ConnectedTime'].mean(), line_width=1,line_dash="dot", line_color="black")
            fig2.add_annotation(x=laadpaaldata1['ConnectedTime'].mean() + 0.75, y=800, text="gemiddelde", showarrow=False)
            
            st.plotly_chart(fig2)
            
        with col3a:
            x = laadpaaldata1["ChargeTime"]
            hist_data = [x]

            group_labels = ['ChargeTime']
            colors = ['rgb(224, 224, 224)']
            
            fig3 = ff.create_distplot(hist_data, group_labels, bin_size=.2, colors= colors)
            
            ig2.update_layout(
                            xaxis=dict(title = 'ChargeTime'),
                            yaxis=dict(title = "Aantal laadsessies"))
            
            st.plotly_chart(fig3)
            

 

#Elektrische auto's
with tab3:
    col1, col2 = st.columns([1, 1])

    with col1:
        elektrischvoertuig = pd.read_csv('Elektrische_voertuigen_2.csv',low_memory=False)
        
        #lege rijen verwijderen en datum format
        elektrischvoertuig = elektrischvoertuig.dropna(axis='columns', how='all')
        elektrischvoertuig['Datum tenaamstelling DT']= pd.to_datetime(elektrischvoertuig['Datum tenaamstelling DT'], format='%m/%d/%Y %H:%M:%S AM')
        
        #grafiek
        elektrischvoertuig = elektrischvoertuig.sort_values(by = 'Datum tenaamstelling DT', ascending = True)
        elektrischvoertuig['year'] = pd.DatetimeIndex(elektrischvoertuig['Datum tenaamstelling DT']).year
        df_perdatum = elektrischvoertuig.groupby('year')['Kenteken'].count().cumsum()
        fig = go.Figure(go.Scatter(x = elektrischvoertuig['year'].unique(), y = df_perdatum, mode = 'lines', line_color = 'black'))
        
        
        
        fig.update_layout(title_text = ("Cumulatieve som van het aantal elektrische auto's per jaar"), font = dict(size = 18), title = dict(y = 0.9, x = 0.5, xanchor = 'center', yanchor = 'top'))
        fig.update_xaxes(title_text = "Jaartal") 
        fig.update_yaxes(title_text = "Aantal elektrische auto's")
        
        # #selectbox
        # var_name = st.radio('Select a variable', ['Log Scale', 'linear Scale' ])
        # var_name_dict = {"linear Scale":'linear','Log Scale':'log'}
        # fig.update_yaxes(type = var_name_dict[var_name])
        
        updatemenus = [
        dict(
            type="dropdown",
            direction="down",
            x = 1.3, y=1,
            buttons=list([
                dict(
                    args=[{"yaxis.type": "linear"}],
                    label="Linear Scale",
                    method="relayout"
                ),
                dict(
                    args=[{"yaxis.type": "log"}],
                    label="Log Scale",
                    method="relayout"
                )
            ])
        ),
        ]  
    
        fig.update_layout(
            updatemenus=updatemenus
        )
        
        st.plotly_chart(fig)
    
        
    with col2:
        st.markdown("**Meest voorkochte auto's**")
        
        merken_elektrischvoertuig2 = elektrischvoertuig.groupby(['Merk', 'Handelsbenaming'], as_index = False).agg({'Kenteken': 'count','Catalogusprijs': 'mean' })
        merken_elektrischvoertuig2.columns = ['Merk', 'Handelsbenaming', 'Aantal keer verkocht', 'Catalogusprijs']
        merken_elektrischvoertuig2 = merken_elektrischvoertuig2.sort_values('Aantal keer verkocht', ascending = False)
        merken_elektrischvoertuig2 = merken_elektrischvoertuig2.reset_index()
        st.dataframe(merken_elektrischvoertuig2[['Merk', 'Handelsbenaming', 'Aantal keer verkocht', 'Catalogusprijs']])
        
    

#footer
html = """
<style>
  #MainMenu {
      visibility: hidden;}
  footer {
      visibility:hidden;}
  footer:after{
      visibility:visible;
      content:'Case 2, group 5: Enrico Olivier, Evelien de Roode, Matthijs van Vliet, Valery Limburg';
      display:block;
      position:relative;
      color:gray;}
</style>
"""
st.markdown(html, unsafe_allow_html= True)