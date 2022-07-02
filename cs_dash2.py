import dash
from dash import dcc, html, Input, Output
import dash_daq as daq
import pandas as pd
import numpy as np 
import dash_bootstrap_components as dbc
import cs_baseline

charts = dbc.Col(
html.Div(
    children=[
        html.Div(
            children=dcc.Graph(
                id="price-chart", config={"displayModeBar": False},
            ),
            className="card",
        ),
    ],
    className="wrapper",
),
)
case_inputs = dbc.Col(
      children=[
          
          html.Div(
              children=[
                  html.Div(children="Number of Kids", className="menu-title"), daq.Slider(id="numkids", min=1,max=5,value=1,handleLabel={"showCurrentValue": True,"label": "kids"},),
                  html.Div(children="Parent A Kid 1 Care Nights", className="menu-title"), daq.Slider(id="a_kid_1_cn_i", min=0,max=365,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent A Kid 2 Care Nights", className="menu-title"), daq.Slider(id="a_kid_2_cn_i", min=0,max=365,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent A Kid 3 Care Nights", className="menu-title"), daq.Slider(id="a_kid_3_cn_i", min=0,max=365,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent A Kid 4 Care Nights", className="menu-title"), daq.Slider(id="a_kid_4_cn_i", min=0,max=365,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent A Kid 5 Care Nights", className="menu-title"), daq.Slider(id="a_kid_5_cn_i", min=0,max=365,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),                  
                  html.Div(children="Kid 1 Age", className="menu-title"), daq.Slider(id="kid_1_age_i", min=0,max=17,value=0,handleLabel={"showCurrentValue": True,"label": "Years"},),
                  html.Div(children="Kid 2 Age", className="menu-title"), daq.Slider(id="kid_2_age_i", min=0,max=17,value=0,handleLabel={"showCurrentValue": True,"label": "Years"},),
                  html.Div(children="Kid 3 Age", className="menu-title"), daq.Slider(id="kid_3_age_i", min=0,max=17,value=0,handleLabel={"showCurrentValue": True,"label": "Years"},),
                  html.Div(children="Kid 4 Age", className="menu-title"), daq.Slider(id="kid_4_age_i", min=0,max=17,value=0,handleLabel={"showCurrentValue": True,"label": "Years"},),
                  html.Div(children="Kid 5 Age", className="menu-title"), daq.Slider(id="kid_5_age_i", min=0,max=17,value=0,handleLabel={"showCurrentValue": True,"label": "Years"},),

              ]
          ),
        ],
      )
      
par_a_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                  html.Div(children="A ATI", className="menu-title"), daq.Slider(id="a_ati_i", min=0,max=300000,value=50000,handleLabel={"showCurrentValue": True,"label": "$"},),
                  html.Div(children="A number of other cases", className="menu-title"), daq.Slider(id="a_othercase_n_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Cases"},),
                  html.Div(children="Parent A Number of  kids  in other cases with less than shared care", className="menu-title"), daq.Slider(id="a_othercase_okids_lsc_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent A Number of kids 12 and under in other cases", className="menu-title"), daq.Slider(id="a_othercase_12l_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent A Number of kids 13 and over in other cases", className="menu-title"), daq.Slider(id="a_othercase_13p_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent A Number of rel deps 12 and under ", className="menu-title"), daq.Slider(id="a_reldep_12l_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent A Number of rel deps 13 and over ", className="menu-title"), daq.Slider(id="a_reldep_13p_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent A ISP", className="menu-title"), dcc.Dropdown(id="a_isp_i", options=[{"label": "Yes", "value": 1},{"label": "No", "value": 0}], value=1,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )

par_b_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                  html.Div(children="Parent B ATI", className="menu-title"), daq.Slider(id="b_ati_i", min=0,max=300000,value=50000,handleLabel={"showCurrentValue": True,"label": "$"},),
                  html.Div(children="Parent B number of other cases", className="menu-title"), daq.Slider(id="b_othercase_n_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Cases"},),
                  html.Div(children="Parent B Number of  kids  in other cases with less than shared care", className="menu-title"), daq.Slider(id="b_othercase_okids_lsc_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Nights"},),
                  html.Div(children="Parent B Number of kids 12 and under in other cases", className="menu-title"), daq.Slider(id="b_othercase_12l_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent B Number of kids 13 and over in other cases", className="menu-title"), daq.Slider(id="b_othercase_13p_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent B Number of rel deps 12 and under ", className="menu-title"), daq.Slider(id="b_reldep_12l_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent B Number of rel deps 13 and over ", className="menu-title"), daq.Slider(id="b_reldep_13p_i", min=0,max=10,value=0,handleLabel={"showCurrentValue": True,"label": "Kids"},),
                  html.Div(children="Parent B ISP", className="menu-title"), dcc.Dropdown(id="b_isp_i", options=[{"label": "Yes", "value": 1},{"label": "No", "value": 0}], value=1,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )
      
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Child Support Formula"
liability_output= dbc.Col(
      children=[ html.Div(id='liability_statement-container'), ],
      )
app.layout = dbc.Container(
    children=[
      html.Div(
        children=[
        html.P(children="👶", className="header-emoji"),
                html.H1(
                    children="Child Support Formula", className="header-title"
                ),
                html.P(
                    children="Calculate how much you are owed",
                    className="header-description",
                ),
        ],
        className="header",
      ),
      dbc.Row(      [ liability_output, charts  ])   ,
      dbc.Row(      [case_inputs,  par_a_inputs ,par_b_inputs,     ])   ,
      dbc.Row(      [    ])   
    ]
)

@app.callback(
    [Output('liability_statement-container', 'children'),Output("price-chart", "figure")],
    [dict(

    numkids = Input('numkids', 'value'),
    a_kid_1_cn_i = Input('a_kid_1_cn_i', 'value'),
    a_kid_2_cn_i = Input('a_kid_2_cn_i', 'value'),
    a_kid_3_cn_i = Input('a_kid_3_cn_i', 'value'),
    a_kid_4_cn_i = Input('a_kid_4_cn_i', 'value'),
    a_kid_5_cn_i = Input('a_kid_5_cn_i', 'value'),
    kid_1_age_i = Input('kid_1_age_i', 'value'),
    kid_2_age_i = Input('kid_2_age_i', 'value'),
    kid_3_age_i = Input('kid_3_age_i', 'value'),
    kid_4_age_i = Input('kid_4_age_i', 'value'),
    kid_5_age_i = Input('kid_5_age_i', 'value'),
    a_ati_i = Input('a_ati_i', 'value'),
    a_othercase_n_i = Input('a_othercase_n_i', 'value'),
    a_othercase_okids_lsc_i = Input('a_othercase_okids_lsc_i', 'value'),
    a_othercase_12l_i = Input('a_othercase_12l_i', 'value'),
    a_othercase_13p_i = Input('a_othercase_13p_i', 'value'),
    a_reldep_12l_i = Input('a_reldep_12l_i', 'value'),
    a_reldep_13p_i = Input('a_reldep_13p_i', 'value'),
    a_isp_i = Input('a_isp_i', 'value'),
    b_ati_i = Input('b_ati_i', 'value'),
    b_othercase_n_i = Input('b_othercase_n_i', 'value'),
    b_othercase_okids_lsc_i = Input('b_othercase_okids_lsc_i', 'value'),
    b_othercase_12l_i = Input('b_othercase_12l_i', 'value'),
    b_othercase_13p_i = Input('b_othercase_13p_i', 'value'),
    b_reldep_12l_i = Input('b_reldep_12l_i', 'value'),
    b_reldep_13p_i = Input('b_reldep_13p_i', 'value'),
    b_isp_i = Input('b_isp_i', 'value'),
    )
    ]
)
def update_liability_statement(kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i,numkids
                ,a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i
                ,a_ati_i,a_othercase_n_i,a_othercase_okids_lsc_i,a_othercase_12l_i,a_othercase_13p_i, a_reldep_12l_i,a_reldep_13p_i,  a_isp_i
                ,b_ati_i,b_othercase_n_i,b_othercase_okids_lsc_i,b_othercase_12l_i,b_othercase_13p_i, b_reldep_12l_i,b_reldep_13p_i,  b_isp_i
                ):

    cs_liability = cs_baseline.cs_baseline(2022,[kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i],numkids
    ,"Parent A",[a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i],a_othercase_n_i,a_othercase_okids_lsc_i, a_isp_i, a_reldep_12l_i,a_reldep_13p_i,a_ati_i,a_othercase_12l_i,a_othercase_13p_i
    ,"Parent B",[0,0,0,0,0],b_othercase_n_i,b_othercase_okids_lsc_i, b_isp_i, b_reldep_12l_i,b_reldep_13p_i,b_ati_i,b_othercase_12l_i,b_othercase_13p_i
    )
    if cs_liability>0: liability_statement = 'Parent A pays Parent B ${:n}'.format(cs_liability)
    else : liability_statement = 'Parent B pays Parent A ${:n}'.format(-cs_liability)
    
    incomes=[]
    liabilities=[]
    marginal=[]
    for i,income in enumerate(range(1,300000,1000)):

        incomes.append(income)
        liabilities.append(cs_baseline.cs_baseline(2022,[kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i],numkids
    ,"Parent A",[a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i],a_othercase_n_i,a_othercase_okids_lsc_i, a_isp_i, a_reldep_12l_i,a_reldep_13p_i,income,a_othercase_12l_i,a_othercase_13p_i
    ,"Parent B",[0,0,0,0,0],b_othercase_n_i,b_othercase_okids_lsc_i, b_isp_i, b_reldep_12l_i,b_reldep_13p_i,b_ati_i,b_othercase_12l_i,b_othercase_13p_i
    ))
                
    price_chart_figure = {
        "data": [
            {
                "x": incomes,
                "y": liabilities,
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    
    
    return([liability_statement,price_chart_figure])

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)