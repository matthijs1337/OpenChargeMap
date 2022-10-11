# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

# pip install sodapy

import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years

import plotly.io as pio
pio.renderers.default = 'browser'


class Provincie:
  def __init__ (self, provincie, longitude, latitude):
    self.provincie = provincie
    self.longitude = longitude
    self.latitude = latitude
    
  def show_all(self):
    print (self.provincie, self.longitude, self.latitude)

st.set_page_config(layout = 'wide')

st.title("Title")
tab1, tab2, tab3 = st.tabs(["OpenChargeMap", "Laadpaaldata", "Elektrische auto's"])


#openChargeMap
with tab1: 
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
    
    
    st.write(f'{querystring}')
    
    response = requests.request("GET", url, headers=headers, params=querystring)
    tekst = response.json()
    Open_Charge_Map=pd.DataFrame(tekst)
        
#######DataCleaning
api_data = Open_Charge_Map
print(api_data.describe())

#import pandas as pd

dfadress = pd.DataFrame(api_data['AddressInfo'].values.tolist())
dfadress

api_data.drop(['AddressInfo'], axis=1)

mergedDf = dfadress.merge(api_data, how='right', left_index=True, right_index=True)
mergedDf

api_clean = mergedDf[['ID_y', 'NumberOfPoints', 'DateCreated', 'UsageCost', 'ID_x', 'Title', 'AddressLine1', 'Town'
                      , 'Postcode', 'CountryID', 'Latitude', 'Longitude']]

api_clean.rename(columns={'ID_y': 'ID', 'ID_x': 'Adress_ID', 'AddressLine1' : 'Adress'})

#Aantal laadpalen
#Per gemeente
api_clean["Town"].value_counts()

def opsplitsen_postcode(value):
    begin = value[0:4]

    if value[5] == '-':
        einde = value[7:11]
        provincie = value[12:]
    else:
        einde = begin
        provincie = value[5:]

#Aantal laadpalen
#Per provincie

#rare waardes eruit halen
    if provincie == 'Utrecht\xa0voorheen\xa0Zuid-Holland':
        provincie = 'Utrecht'


    return [int(begin), int(einde), provincie] 

def postcode_nummers(value):
    value = str(value)

    if len(value) > 4:
        return int(value[0:4])
    else:
        return 1001
      
postcode_nummers("1394 Noord-Holland")

postcode_provincie = pd.read_excel('postcode_provincie.xls',index_col=None)
postcode_provincie.head()

#importeren
postcode_provincie = pd.read_excel('postcode_provincie.xls',index_col=None)

#opsplitsen
postcode_provincie['list'] = postcode_provincie.apply(lambda x: opsplitsen_postcode(x['aanelkaar']), axis = 1)
df_data = pd.DataFrame(postcode_provincie['list'].values.tolist(), index=postcode_provincie.index)
postcode_provincie = pd.concat([postcode_provincie, df_data], axis=1).drop('list', axis=1)
postcode_provincie.columns = ['orgineel', "begin", 'einde', 'provincie']
postcode_provincie.head()

postcode = []
provincie = []

row = 0
for i, row in postcode_provincie.iterrows():
    lijst = (row.einde - row.begin+1)* [row.provincie]
    lijst2 = [*range(row.begin, row.einde+1)]
    provincie += lijst
    postcode += lijst2

print(len(postcode))
print(len(provincie))

dict = {'postcode': postcode, 'provincie': provincie}  
df = pd.DataFrame(dict)
df

postcode_provincie['provincie'].unique() #Alle rare waardes zijn eruit gehaald

#df5
df5 = pd.read_csv("jsonwoonplaatsen.csv")
df5.head()

df5["Provincie"].value_counts()

Provincie = df5[['Plaats', 'Provincie']]
Provincie.head()

#df6
df6 = api_clean.merge(Provincie, how='left', left_on = 'Town', right_on = 'Plaats')
df6[["Town","Plaats","Provincie"]]

#Visualiseer data op een kaart
import folium
from folium.plugins import MarkerCluster



m = folium.Map(location=[52.377956, 4.897070], zoom_start=7)

marker_cluster = MarkerCluster().add_to(m)

for i, x in api_clean.iterrows():
    folium.Marker(location=[x['Latitude'], x['Longitude']],
                        popup="<strong>" + x['Title'] +"<strong>",
                        tooltip='Klik hier om de popup te zien',
                        fill_opacity=0.7,
                        fill= True
                        ).add_to(marker_cluster)

m

st.dataframe(clean_api)

#Laadpaaldata
with tab2:
    st.markdown("hi")

#Elektrische auto's
with tab3:
    elektrischvoertuig = pd.read_csv('Elektrische_voertuigen.csv',low_memory=False)
    
    #lege rijen verwijderen en datum format
    elektrischvoertuig = elektrischvoertuig.dropna(axis='columns', how='all')
    elektrischvoertuig['Datum tenaamstelling DT']= pd.to_datetime(elektrischvoertuig['Datum tenaamstelling DT'], format='%m/%d/%Y %H:%M:%S AM')
    
    #grafiek
    elektrischvoertuig = elektrischvoertuig.sort_values(by = 'Datum tenaamstelling DT', ascending = True)
    elektrischvoertuig['year'] = pd.DatetimeIndex(elektrischvoertuig['Datum tenaamstelling DT']).year
    df_perdatum = elektrischvoertuig.groupby('year')['Kenteken'].count().cumsum()
    fig = go.Figure(go.Scatter(x = elektrischvoertuig['year'].unique(), y = df_perdatum, mode = 'lines', line_color = 'black'))
    
    fig.update_yaxes(type="log")
    fig.update_layout(title_text = ("Number of electric cars sold"), 
                      font = dict(size = 18), title = dict(y = 0.9, x = 0.5, xanchor = 'center', yanchor = 'top'))
    fig.update_xaxes(title_text = "Year") 
    fig.update_yaxes(title_text = "Number of electric cars in log")
    
    st.plotly_chart(fig)


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
