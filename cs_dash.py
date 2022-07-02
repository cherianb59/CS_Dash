import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np 

data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

app.layout = html.Div(
    children=[
      html.Div(
        children=[
        html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
        ],
        className="header",
      ),
      html.Div(
      children=[
          html.Div(
              children=[
                  html.Div(children="Region", className="menu-title"),
                  dcc.Dropdown(
                      id="region-filter",
                      options=[
                          {"label": region, "value": region}
                          for region in np.sort(data.region.unique())
                      ],
                      value="Albany",
                      clearable=False,
                      className="dropdown",
                  ),
              ]
          ),
          html.Div(
              children=[
                  html.Div(children="Type", className="menu-title"),
                  dcc.Dropdown(
                      id="type-filter",
                      options=[
                          {"label": avocado_type, "value": avocado_type}
                          for avocado_type in data.type.unique()
                      ],
                      value="organic",
                      clearable=False,
                      searchable=False,
                      className="dropdown",
                  ),
              ],
          ),
          html.Div(
              children=[
                  html.Div(
                      children="Date Range",
                      className="menu-title"
                      ),
                  dcc.DatePickerRange(
                      id="date-range",
                      min_date_allowed=data.Date.min().date(),
                      max_date_allowed=data.Date.max().date(),
                      start_date=data.Date.min().date(),
                      end_date=data.Date.max().date(),
                  ),
              ]
          ),
      ],
      className="menu",
  ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AveragePrice"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Total Volume"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            },
        ),
    ]
)
if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0', port=5000)