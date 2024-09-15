from dash_app.match_stats import match_stats_layout
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

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Input(id="search_gamertag", type="text", placeholder="", debounce=True),
    dcc.Dropdown(id='dropdown-selection'),
    html.Div(id="match_data")
]


@callback(
    # Output('dropdown-selection', 'options'),
    Input('search_gamertag', 'value'),
    background=True,
    manager=background_callback_manager,
)
def get_matches(gamer_tag):
    if not gamer_tag:
        pass
    print(f"started {datetime.now()}")
    match_history = asyncio.run(get_match_history(gamer_tag))
    options = []
    for match in match_history:
        gamemode = asyncio.run(get_gamemode(match.match_info.ugc_game_variant.asset_id, match.match_info.ugc_game_variant.version_id)).public_name
        map_name = asyncio.run(get_map(match.match_info.map_variant.asset_id, match.match_info.map_variant.version_id)).public_name
        option = {'label': f"{gamemode} - {map_name}", 'value': f"{match.match_id}"}
        options.append(option)
        set_props('dropdown-selection', {'options': options})
    print(f"done {datetime.now()}")
    # return options


@callback(
    Output('match_data', 'children'),
    Input('dropdown-selection', 'value')
)
def get_stats(match_id):
    match_stats = asyncio.run(get_match(match_id))
    return match_stats_layout(match_stats)


if __name__ == '__main__':
    app.run(debug=True)
