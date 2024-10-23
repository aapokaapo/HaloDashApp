from dash_app import match_data
from dash_app import search_bar
import plotly.express as px
import pandas as pd
from spnkr_app import *
import asyncio
from aiohttp import ClientResponseError

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
    html.Hr(),
    html.Div(id="search_bar", children=search_bar.set_layout()),
    html.Hr(),
    dcc.Loading(html.Div(id='match_data')),
    dcc.Location(id='url', refresh='callback-nav')
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
    try:
        match_history = asyncio.run(get_match_history(gamer_tag, count, start))
    except ClientResponseError as error:
        return
    search_bar.update_options(match_history, start, count)
    return


@callback(
    [
        Output('url', 'pathname'),
        Output('url', 'refresh'),
    ],
    Input('dropdown-selection', 'value')
)
def get_stats(match_id):
    if not match_id:
        return '', False
    return f'/{match_id}', 'callback-nav'
    
    
@callback(
    Output('match_data', 'children'),
    [
        Input('url', 'href'),
        Input('url', 'pathname')
    ]
)
def update_stats(url, match_id):
    if not match_id and url:
        match_id = url.replace('https://aapokaapostats.site', '')
    if not match_id:
        return None
    try:
        match_stats = asyncio.run(get_match(match_id.strip('/')))
    except ClientResponseError as error:
        return html.Div(f'Match ID {match_id} caused an error while creating the stats. Error: {error}')
    stats_container = match_data.set_layout(match_stats)
    return stats_container


if __name__ == '__main__':
    app.run(debug=True)


