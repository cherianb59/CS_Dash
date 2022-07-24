import dash
from dash import dcc, html, Input, Output
import dash_daq as daq
import pandas as pd
import numpy as np 
import dash_bootstrap_components as dbc

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask

def child_age_div(age):
    age_str = str(age)
    return(html.Div(children="Kid {} Age".format(age), className="menu-title"), dcc.Slider(id="kid_{}_age_i".format(age), min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},) )
case_inputs = dbc.Col(
      children=[
          
          html.Div(
              children=[
                  html.Div(children="Number of Kids", className="menu-title"), dcc.Slider(id="numkids", min=1,max=5,value=1,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 1 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_1_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 2 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_2_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 3 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_3_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 4 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_4_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 5 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_5_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),                  
                  *[child_age_div(i) for i in range(1,6) ]
#                  html.Div(children="Kid 1 Age", className="menu-title"), dcc.Slider(id="kid_1_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
#                  html.Div(children="Kid 2 Age", className="menu-title"), dcc.Slider(id="kid_2_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
#                  html.Div(children="Kid 3 Age", className="menu-title"), dcc.Slider(id="kid_3_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
#                  html.Div(children="Kid 4 Age", className="menu-title"), dcc.Slider(id="kid_4_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
#                  html.Div(children="Kid 5 Age", className="menu-title"), dcc.Slider(id="kid_5_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  
              ]
          ),
        ],
      )
case_inputs2 = dbc.Col(
      children=[
          
          html.Div(
              children=[
                  html.Div(children="Number of Kids", className="menu-title"), dcc.Slider(id="numkids", min=1,max=5,value=1,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 1 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_1_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 2 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_2_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 3 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_3_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 4 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_4_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Parent A Kid 5 Care Nights", className="menu-title"), dcc.Slider(id="a_kid_5_cn_i", min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},),                  
                  html.Div(children="Kid 1 Age", className="menu-title"), dcc.Slider(id="kid_1_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Kid 2 Age", className="menu-title"), dcc.Slider(id="kid_2_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Kid 3 Age", className="menu-title"), dcc.Slider(id="kid_3_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Kid 4 Age", className="menu-title"), dcc.Slider(id="kid_4_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Kid 5 Age", className="menu-title"), dcc.Slider(id="kid_5_age_i", min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  
              ]
          ),
        ],
      )
import pprint
pp = pprint.PrettyPrinter(indent=4, width=80)
pp.pprint(case_inputs)
  pp.pprint(case_inputs2)