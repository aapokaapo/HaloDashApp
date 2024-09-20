from dash_app import match_data
from dash_app import search_bar
import plotly.express as px
import pandas as pd
from spnkr_app import *
import asyncio

from datetime import datetime

import os
from dash import Dash, DiskcacheManager, CeleryManager, Input, Output, html, callback, dcc, set_props

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)

else:
    # Diskcache for non-production apps when developing locally
    print("Redis & Celery not available. Using Diskcache")
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

app = Dash(__name__)

server = app.server

app.layout = [
    html.H1(id="header", children="AapoKaapo's Stats Site", style={'textAlign': 'center'}),
    html.P("This site is still in early development. This site does not use cookies(yet) and thus no data is saved. The site may or may not work. -AapoKaapo"),
    html.Div(dcc.Link(href='https://github.com/aapokaapo/HaloDashApp', target='header')),
    html.Div(id="search_bar", children=search_bar.set_layout()),
    html.Div(id="match_data")
]


@callback(
    # Output('dropdown-selection', 'options'),
    [
        Input('search_gamertag', 'value'),
        Input('count', 'value'),
        Input('start', 'value'),
    ],
    background=True,
    cancel=[
        Input('search_gamertag', 'value'),
        Input('count', 'value'),
        Input('count', 'value'),
    ],
    manager=background_callback_manager,
)
def get_matches(gamer_tag, count, start):
    if not gamer_tag:
        return
    set_props('dropdown-selection', {'options': []})
    match_history = asyncio.run(get_match_history(gamer_tag, count, start))
    search_bar.update_options(match_history, start)


@callback(
    Output('match_data', 'children'),
    Input('dropdown-selection', 'value')
)
def get_stats(match_id):
    if not match_id:
        return None
    match_stats = asyncio.run(get_match(match_id))
    return match_data.set_layout(match_stats)


if __name__ == '__main__':
    app.run(debug=True)
