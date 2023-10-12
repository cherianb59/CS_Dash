import dash
from dash import dcc, html, Input, Output ,dash_table
import dash_daq as daq
import pandas as pd
import numpy as np 
import dash_bootstrap_components as dbc
import cs_baseline
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask

server = Flask(__name__)
server.secret_key ='Vne24vU3rI+092ykVwdBRw=='

app = dash.Dash(name = __name__,
                server = server,
                title='Child Support Calculator',
                external_stylesheets=[dbc.themes.FLATLY]
               )

server = app.server 

# HELPER FUNCTIONS 

def child_age_div(age):
    return(html.Div(children=f"Kid {age} age", className="menu-title"), dcc.Slider(id=f"kid_{age}_age_i", min=0,max=17,value=0,step=1,marks={ m: str(m) for m in slider_range(0,17,2) },tooltip={"placement": "bottom", "always_visible": False},) )

def child_care_nights_div(nights):
    return(html.Div(children=f"Your nights of care for kid {nights}", className="menu-title"), dcc.Slider(id=f"a_kid_{nights}_cn_i", min=0,max=365,step=1,value=365,marks={ m: str(m) for m in slider_range(0,365,50) },tooltip={"placement": "bottom", "always_visible": False},))

def slider_range(min,max,step=1):
  sr = list(range(min,max+1,step))
  if sr[-1] != max: sr[-1] = max
  return(sr)

def make_tooltip(id,text):
    return dbc.Tooltip(
        text,
        target=id 
        ,placement="top")
  
#LAYOUT

header = dbc.Row(class_name='main-header-outer-container', children=[
            dbc.Col(class_name='main-header-inner-container', children=[
                html.Div(className='main-header-title-container', children=[
                    html.Div(className='main-header-title', children='Child Support Calculator'),
                    html.Div(className='main-header-description', children='Figure out how much Child Support you are entitled to'),
                ])
            ]),
        ])



intro = dbc.Col(
      children=[ html.Div(id='introduction-container',
      children=[html.P(children="Enter your details about the kids you have with the other parent, your details (income and other kids you have) and the other parent's details (their income and other kids they have)."),]
      ), ]
      ,
      )
      
liability_output= dbc.Col(
      children=[ html.P(html.Div(id='liability_statement-container')), ]
      ,
      )

  
case_inputs = dbc.Col(
      children=[
          
          html.Div(
              children=[
                  html.Div(children="Number of Kids with other parent", className="menu-title"), dcc.Slider(id="numkids", min=1,max=5,value=1,step=1,tooltip={"placement": "bottom", "always_visible": False},),
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
                  html.Div(children="Your pre-tax income last financial year", className="menu-title",id="a_ati_tt"),make_tooltip(id="a_ati_tt",text="Your taxable income plus reportable fringe benefits, target foreign income, total net investment loss, tax free pensions or benefits and reportable superannuation contributions"), dcc.Slider(id="a_ati_i", min=0,max=300000,value=50000,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support cases you have", className="menu-title",id="a_othercase_n_tt"),make_tooltip(id="a_othercase_n_tt",text="How many ex-partners you had kids with"), dcc.Slider(id="a_othercase_n_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),                  
                  html.Div(children="Number of other child support pre-teenagers", className="menu-title",id="a_othercase_12l_tt"),make_tooltip(id="a_othercase_12l_tt",text="Number of kids in other child support cases that are 12 or less"), dcc.Slider(id="a_othercase_12l_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support teenagers", className="menu-title",id="a_othercase_13p_tt"),make_tooltip(id="a_othercase_13p_tt",text="Number of kids in other child support cases that are 13 or over"), dcc.Slider(id="a_othercase_13p_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of non-child support pre-teenagers", className="menu-title",id="a_reldep_12l_tt"),make_tooltip(id="a_reldep_12l_tt",text="Number of kids in your current relationship that are 12 or less"), dcc.Slider(id="a_reldep_12l_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of non-child support teenagers", className="menu-title",id="a_reldep_13p_tt"),make_tooltip(id="a_reldep_13p_tt",text="Number of kids in your current relationship that are 13 or older"), dcc.Slider(id="a_reldep_13p_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support kids where you have less than 128 nights of care", className="menu-title",id="a_othercase_okids_lsc_tt"),make_tooltip(id="a_othercase_okids_lsc_tt",text="Number of kids in other child support cases where you have custody less than 128 nights in a year"), dcc.Slider(id="a_othercase_okids_lsc_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Did you get Income Support last financial year?", className="menu-title",id="a_isp_tt"),make_tooltip(id="a_isp_tt",text="Did you receive Youth Allowance, Austudy Payment, Jobseeker Payment, Special Benefit, Parenting Payment (Partnered), Age Pension, Disability Support Pension, Carer Payment or Parenting Payment (Single) in the previous financial year?"), dcc.Dropdown(id="a_isp_i", options=[{"label": "Yes", "value": 1},{"label": "No", "value": 0}], value=1,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )

par_b_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                  html.Div(children="Other parent's pre-tax income last financial year", className="menu-title",id="b_ati_tt"),make_tooltip(id="b_ati_tt",text="Other parent's taxable income plus reportable fringe benefits, target foreign income, total net investment loss, tax free pensions or benefits and reportable superannuation contributions"), dcc.Slider(id="b_ati_i", min=0,max=300000,value=50000,tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Number of other child support cases other parent has", className="menu-title",id="b_othercase_n_tt"),make_tooltip(id="b_othercase_n_tt",text="How many other ex-partners the other parent had kids with"), dcc.Slider(id="b_othercase_n_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},), 
                  html.Div(children="Other parent's number of other child support pre-teenagers", className="menu-title",id="b_othercase_12l_tt"),make_tooltip(id="b_othercase_12l_tt",text="Other parent's number of kids in other child support cases that are 12 or less"), dcc.Slider(id="b_othercase_12l_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent's number of other child support teenagers", className="menu-title",id="b_othercase_13p_tt"),make_tooltip(id="b_othercase_13p_tt",text="Other parent's number of kids in other child support cases that are 13 or over"), dcc.Slider(id="b_othercase_13p_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent's number of non-child support pre-teenagers", className="menu-title",id="b_reldep_12l_tt"),make_tooltip(id="b_reldep_12l_tt",text="Other parent's number of kids in your current relationship that are 12 or less"), dcc.Slider(id="b_reldep_12l_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent's number of non-child support teenagers", className="menu-title",id="b_reldep_13p_tt"),make_tooltip(id="b_reldep_13p_tt",text="Other parent's number of kids in their current relationship that are 13 or older"), dcc.Slider(id="b_reldep_13p_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Other parent's number of child support kids where they have less than 128 nights of care", className="menu-title",id="b_othercase_okids_lsc_tt"),make_tooltip(id="b_othercase_okids_lsc_tt",text="Other parent's number of kids in other child support cases where they have custody less than 128 nights in a year"), dcc.Slider(id="b_othercase_okids_lsc_i", min=0,max=10,value=0,step=1,marks={ m: str(m) for m in slider_range(0,10,2) },tooltip={"placement": "bottom", "always_visible": False},),
                  html.Div(children="Did the other parent get Income Support last financial year?", className="menu-title",id="b_isp_tt"),make_tooltip(id="b_isp_tt",text="Did the other parent receive Youth Allowance, Austudy Payment, Jobseeker Payment, Special Benefit, Parenting Payment (Partnered), Age Pension, Disability Support Pension, Carer Payment or Parenting Payment (Single) in the previous financial year?"), dcc.Dropdown(id="b_isp_i", options=[{"label": "Yes", "value": 1},{"label": "No", "value": 0}], value=1,clearable=False,searchable=False,className="dropdown",),
              ]
          ),
        ],
      )

formula_changes = dbc.Col(children=[html.Div(children="Change the Child Support Formula with the options below", className="header2" )])

income_bands_inputs = dbc.Col(
      children=[        
          html.Div(
              children=[
                html.Div(children="Income bands of the cost of children taper", className="menu-title"),
                dcc.RangeSlider(id="income_bands_i", min = 0, max = 300000, step = 1000 ,marks = {x:("$"+str(x)) for x in range(0,300000,20000)}, value = cs_baseline.default_income_bands, pushable=1000,tooltip={"placement": "bottom", "always_visible": False},),
              ]
          ),
        ],
      )
                
liability_chart = html.Div(
            children=dcc.Graph(id="price-chart", ),
            className="card",
        )

coct_chart = html.Div(
            children=dcc.Graph(id="coct-chart", ),
            className="card",
        )

taper_types = [("12l",1),("12l",2),("12l",3),("13p",1),("13p",2),("13p",3)]
#formatting
child_ages_f = {"12l":"less than 12","13p":" over 13","mix":"of mixed ages"}
num_child_f = {1:"1 child",2:"2 children",3:"3 (or more) children"}

tapers_table=dbc.Col(
        html.Div(children=[html.Div(children="Cost of children tapers", className="menu-title"), 
            dash_table.DataTable(
                id='tapers_i',
                columns=[{
                #id column-12l-1
                    'name': f'{num_child_f[i[1]]} {child_ages_f[i[0]]}',
                    'id': f'column-{i[0]}-{i[0]}',
                    'deletable': False,
                    'renamable': False,
                    'type': 'numeric'
                } for i in taper_types] 
                ,
                data=[
                #id column-12l-1, : lookup default taper rate
                    {f'column-{i[0]}-{i[1]}': cs_baseline.default_tapers[i][j] for i in taper_types}
                    for j in range(6)
                ],
                editable=True
            )
    ])
    )
    
                
app.title = "Child Support Formula"
app.layout = dbc.Container(fluid=True, class_name='app-container',
    children=[
      header,
      dbc.Row( [ intro ])   ,
      dbc.Row( [ liability_output ])   ,      
      dbc.Row( [ case_inputs,  par_a_inputs ,par_b_inputs, ])   ,
      dbc.Row( [ liability_chart ])   ,
      dbc.Row( [ formula_changes])   ,
      dbc.Row( [ income_bands_inputs]) ,  
      dbc.Row( [ tapers_table ]) ,  
      dbc.Row( [ coct_chart ]) ,  
    ]
)

##TODO there should be an easier way to do this.
@app.callback(
    [Output('liability_statement-container', 'children'),Output("price-chart", "figure"),Output("coct-chart", "figure")],
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
    income_bands_i = Input('income_bands_i', 'value'),
    tapers_d = Input('tapers_i', 'data'),
    tapers_c = Input('tapers_i', 'columns'),
    )
    ]
)
def update_liability_statement(kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i,numkids
                ,a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i
                ,a_ati_i,a_othercase_n_i,a_othercase_okids_lsc_i,a_othercase_12l_i,a_othercase_13p_i, a_reldep_12l_i,a_reldep_13p_i,  a_isp_i
                ,b_ati_i,b_othercase_n_i,b_othercase_okids_lsc_i,b_othercase_12l_i,b_othercase_13p_i, b_reldep_12l_i,b_reldep_13p_i,  b_isp_i
                ,income_bands_i,tapers_d,tapers_c):

    
    taper = {i:[0]*6 for i in taper_types}
    for i in range(6):
        for k in taper_types:
            raw_in = tapers_d[i][f'column-{k[0]}-{k[1]}']
            taper[k][i] = float(raw_in)
 
    #calculate mix
    taper["mix",1] = [0] * len(taper["12l",1])
    taper["mix",2] = np.divide( np.add(taper["12l",2]  , taper["13p",2]),2)
    taper["mix",3] = np.divide( np.add(taper["12l",3]  , taper["13p",3]),2)

    tapers = str(taper)
    
    cs_liability_parms= dict(year=2022, ages= [kid_1_age_i,kid_2_age_i,kid_3_age_i,kid_4_age_i,kid_5_age_i], nchild=numkids
    ,a_name="Parent A",a_cn=[a_kid_1_cn_i,a_kid_2_cn_i,a_kid_3_cn_i,a_kid_4_cn_i,a_kid_5_cn_i],a_othercase_n=a_othercase_n_i,a_oth_lsc=a_othercase_okids_lsc_i,a_isp=a_isp_i,a_reldep_12l=a_reldep_12l_i, a_reldep_13p=a_reldep_13p_i,a_ati=a_ati_i, a_othercase_12l=a_othercase_12l_i, a_othercase_13p=a_othercase_13p_i
    ,b_name="Parent B",b_cn=[0,0,0,0,0],b_othercase_n=b_othercase_n_i,b_oth_lsc=b_othercase_okids_lsc_i,b_isp=b_isp_i,b_reldep_12l=b_reldep_12l_i, b_reldep_13p=b_reldep_13p_i,b_ati=b_ati_i, b_othercase_12l=b_othercase_12l_i, b_othercase_13p=b_othercase_13p_i
    ,income_bands=income_bands_i,tapers=taper
    )
    cs_results = cs_baseline.cs_baseline(**cs_liability_parms)
    cs_entitlement = -cs_results['liability']
    
    if cs_entitlement>0: liability_statement = 'The other parent owes you ${:,.0f} per year'.format(cs_entitlement)
    else : liability_statement = 'You owe the other parent ${:,.0f} per year'.format(-cs_entitlement)
    
    #remove a_ati from the dictionary, then pass this to the loop which calculates cs liability for a range of a ati and get the marginal change
    cs_liability_parms.pop('a_ati', None)
    incomes=[]
    entitlements=[]
    marginal=[]
    coct = []
    #numpy vectoristion is not much faster
    for i,income in enumerate(range(0,300000,1000)):

        cs_results = cs_baseline.cs_baseline(**cs_liability_parms,a_ati=income)
        incomes.append(income)
        entitlements.append(-cs_results['liability'])
        coct.append(cs_results['basic_coc'])
        if i == 0 : marginal.append(0)
        else : marginal.append(max(min((entitlements[i]-entitlements[i-1])/(incomes[i]-incomes[i-1]),1),-0.125))       
        
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces (lines)
    fig.add_trace(
        go.Scatter(x=incomes, y=marginal, name="Marginal change in entitlement"),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=incomes, y=entitlements, # replace with your own data source
        name="Entitlement"), secondary_y=False,
    )
        
    fig.update_layout(
    template="simple_white",
    margin=dict(l=0, r=0, t=50, b=0),

    )
    # Add figure title
    fig.update_layout(title_text="Your pre-tax income vs how much you are entitled to")

    # Set x-axis title
    fig.update_xaxes(title_text="Your pre-tax income",tickprefix = '$', tickformat = ',.0f')

    # Set y-axes titles   
    fig.update_yaxes(title_text="How much the other parent owes you", tickprefix = '$', tickformat = ',.0f',secondary_y=False)
    
    fig.update_yaxes(title_text="", secondary_y=True)
    fig.update_yaxes(tickformat=",.0%", secondary_y=True)
    #fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.0f', secondary_y=True)
    
    fig.update_layout(
    legend=dict(
        x=0.7,
        y=0.9,
        bgcolor="rgba(0,0,0,0)",
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
    )
  )
    coct_fig = make_subplots()

    coct_fig.add_trace(
	go.Scatter(x=incomes, y=coct, # replace with your own data source
	name="Cost of the Children"),
	)

    coct_fig.update_layout(
    template="simple_white",
    margin=dict(l=0, r=0, t=50, b=0),
    )
	
    coct_fig.update_layout(title_text="Your pre-tax income vs Cost of the children")

    coct_fig.update_xaxes(title_text="Your pre-tax income",tickprefix = '$', tickformat = ',.0f')

    coct_fig.update_yaxes(title_text="The cost of the children", tickprefix = '$', tickformat = ',.0f',rangemode="tozero")

    coct_fig.update_layout(
    legend=dict(
        x=0.7,
        y=0.9,
        bgcolor="rgba(0,0,0,0)",
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
    )
  )

    return([liability_statement,fig,coct_fig])

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)