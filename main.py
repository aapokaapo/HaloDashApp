from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from spnkr_app import get_match, get_user
import asyncio

match_id = "d3f1f6e4-44b9-4f0e-b43c-fe475daf4060"

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    user = asyncio.run(get_user("AapoKaapo"))
    return px.line(dff, x='year', y='pop')


if __name__ == '__main__':
    app.run(debug=True)