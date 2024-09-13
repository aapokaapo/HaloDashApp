from dash import Dash, html, dcc, callback, Output, Input
from dash_app.match_stats import match_stats_layout
import plotly.express as px
import pandas as pd
from spnkr_app import *
import asyncio

from datetime import datetime

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Input(id="search_gamertag", type="text", placeholder="", debounce=True),
    dcc.Dropdown(id='dropdown-selection'),
    html.Div(id="match_data")
]


@callback(
    Output('dropdown-selection', 'options'),
    Input('search_gamertag', 'value')
)
def get_matches(gamer_tag):
    print(f"started {datetime.now()}")
    match_history = asyncio.run(get_match_history(gamer_tag))
    options = [{'label': f"{asyncio.run(get_gamemode(match.match_info.ugc_game_variant.asset_id, match.match_info.ugc_game_variant.version_id)).public_name} - {asyncio.run(get_map(match.match_info.map_variant.asset_id, match.match_info.map_variant.version_id)).public_name}", 'value': f"{match.match_id}"} for match in match_history]
    print(f"done {datetime.now()}")
    return options


@callback(
    Output('match_data', 'children'),
    Input('dropdown-selection', 'value')
)
def get_stats(match_id):
    match_stats = asyncio.run(get_match(match_id))
    return match_stats_layout(match_stats)


if __name__ == '__main__':
    app.run(debug=True)
