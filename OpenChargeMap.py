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
url = https://api.openchargemap.io/v3




