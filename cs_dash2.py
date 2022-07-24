import dash
from dash import dcc, html, Input, Output
import dash_daq as daq
import pandas as pd
import numpy as np 
import dash_bootstrap_components as dbc
import cs_baseline
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask

server = Flask(__name__)
server.secret_key ='test'


app = dash.Dash(name = __name__, server = server, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server 

liability_output= dbc.Col(
      children=[ html.Div(id='liability_statement-container'), ]
      ,width=2
      ,
      )

liability_chart = dbc.Col(
html.Div(
    children=[
        html.Div(
            children=dcc.Graph(id="price-chart", ),
            className="card",
        ),
    ],
    className="wrapper",
), width=10,
)

def child_age_div(age):
    return(html.Div(children="Kid {} age".format(age), className="menu-title"), dcc.Slider(id="kid_{}_age_i".format(age), min=0,max=17,value=0,step=1,tooltip={"placement": "bottom", "always_visible": False},) )

def child_care_nights_div(nights):
    return(html.Div(children="Your nights of care for kid {}".format(nights), className="menu-title"), dcc.Slider(id="a_kid_{}_cn_i".format(nights), min=0,max=365,value=0,tooltip={"placement": "bottom", "always_visible": False},))
    
case_inputs = dbc.Col(
      children=[
          
          html.Div(
              children=[
                  html.Div(children="Number of Kids", className="menu-title"), dcc.Slider(id="numkids", min=1,max=5,value=1,step=1,tooltip={"placement": "bottom", "always_visible": False},),
                  *[element  for i in range(1,6) for element in child_care_nights_div(i)],
                  *[element  for i in range(1,6) for element in child_age_div(i)]
                  
              ]
          ),
        ],
      )
      
par_a_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                  html.Div(children="Your pre-tax income last financial year", className="menu-title"), dcc.Slider(id="a_ati_i", min=0,max=300000,value=50000,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support cases you have", className="menu-title"), dcc.Slider(id="a_othercase_n_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),                  
                  html.Div(children="Other child support pre-teenagers", className="menu-title"), dcc.Slider(id="a_othercase_12l_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other child support teenagers", className="menu-title"), dcc.Slider(id="a_othercase_13p_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of non-child support pre-teenagers", className="menu-title"), dcc.Slider(id="a_reldep_12l_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of non-child support teenagers", className="menu-title"), dcc.Slider(id="a_reldep_13p_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of kids in other cases with less than 128 nights of care", className="menu-title"), dcc.Slider(id="a_othercase_okids_lsc_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Did you get Income Support last financial year?", className="menu-title"), dcc.Dropdown(id="a_isp_i", options=[{"label": "Yes", "value": 1},{"label": "Yes", "value": 0}], value=0,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )

par_b_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                  html.Div(children="Other parents pre-tax income last financial year", className="menu-title"), dcc.Slider(id="b_ati_i", min=0,max=300000,value=50000,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support cases other parent has", className="menu-title"), dcc.Slider(id="b_othercase_n_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),                  
                  html.Div(children="Other parent other child support pre-teenagers", className="menu-title"), dcc.Slider(id="b_othercase_12l_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent other child support teenagers", className="menu-title"), dcc.Slider(id="b_othercase_13p_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent number of non-child support pre-teenagers", className="menu-title"), dcc.Slider(id="b_reldep_12l_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent number of non-child support teenagers", className="menu-title"), dcc.Slider(id="b_reldep_13p_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent number of kids in other cases with less than 128 nights of care", className="menu-title"), dcc.Slider(id="b_othercase_okids_lsc_i", min=0,max=10,value=0,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Did the other parent get Income Support last financial year?", className="menu-title"), dcc.Dropdown(id="b_isp_i", options=[{"label": "Yes", "value": 1},{"label": "No", "value": 0}], value=0,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )
      
app.title = "Child Support Formula"
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
      dbc.Row(      [ liability_output, liability_chart  ])   ,
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

    cs_liability_parms= dict(year=2022, ages= [kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i], nchild=numkids
    ,a_name="Parent A",a_cn=[a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i],a_othercase_n=a_othercase_n_i,a_oth_lsc=a_othercase_okids_lsc_i,a_isp=a_isp_i,a_reldep_12l=a_reldep_12l_i, a_reldep_13p=a_reldep_13p_i,a_ati=a_ati_i, a_othercase_12l=a_othercase_12l_i, a_othercase_13p=a_othercase_13p_i
    ,b_name="Parent B",b_cn=[0,0,0,0,0],b_othercase_n=b_othercase_n_i,b_oth_lsc=b_othercase_okids_lsc_i,b_isp=b_isp_i,b_reldep_12l=b_reldep_12l_i, b_reldep_13p=b_reldep_13p_i,b_ati=b_ati_i, b_othercase_12l=b_othercase_12l_i, b_othercase_13p=b_othercase_13p_i

    )
    cs_liability = cs_baseline.cs_baseline(**cs_liability_parms)['liability']
    
    if cs_liability>0: liability_statement = 'You owe the other parent ${:n} per year'.format(cs_liability)
    else : liability_statement = 'The other parent owes you ${:n} per year'.format(-cs_liability)
    
    #remove a_ati from the dictionary, then pass this to the loop which calculates cs liability for a range of a ati and get the marginal change
    cs_liability_parms.pop('a_ati', None)
    incomes=[]
    liabilities=[]
    marginal=[]
    
    #numpy vectoristion is not much faster
    for i,income in enumerate(range(0,300000,1000)):

        incomes.append(income)
        liabilities.append(cs_baseline.cs_baseline(**cs_liability_parms,a_ati=income)['liability'])
        if i == 0 : marginal.append(0)
        else : marginal.append(100*max(min((liabilities[i]-liabilities[i-1])/(incomes[i]-incomes[i-1]),0.25),-0.25))       
        
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=incomes, y=liabilities, # replace with your own data source
        name="Liability"), secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=incomes, y=marginal, name="Marginal change in liability"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(title_text="Your income vs how much you owe")

    # Set x-axis title
    fig.update_xaxes(title_text="Your income")

    # Set y-axes titles
    fig.update_yaxes(title_text="", secondary_y=False)
    fig.update_yaxes(title_text="", secondary_y=True)
    
    return([liability_statement,fig])

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)