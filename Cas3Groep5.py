# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:59:05 2022

@author: matth
"""

#importeren van functies

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

import datetime as dt
from dateutil.relativedelta import relativedelta # to add days or years

import plotly.io as pio
pio.renderers.default = 'browser'

#url van api

response = requests.get('https://api.openchargemap.io/v3')

response
headers = {
 #"X-RapidAPI-Key":"f63be25ec8msh09be29d15fcc4fbp1f0f6ejsn82d64b7f3674",
 "X-RapidAPI-Key": "a929aa606bmsh42432cc9b369422p1b8238jsnce8e2abf2f38",
 "X-RapidAPI-Host": "https://openchargemap.org/site"}



