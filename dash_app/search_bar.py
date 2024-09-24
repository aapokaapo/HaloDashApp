from dash import html, dcc, set_props
from spnkr_app import get_map, get_gamemode
import asyncio


def set_layout():
    layout = html.Div(
        [
            dcc.Input(id="search_gamertag", type="text", placeholder="Search for Gamer Tag...", debounce=True),
            html.Div(["Count", dcc.Input(id="count", type="number", value=25, min=1, max=25, name="Count", step=1, debounce=True)]),
            html.Div(["Start", dcc.Input(id="start", type="number", value=0, min=0, name="Start", step=1, debounce=True)]),
            dcc.Dropdown(id='dropdown-selection'),
        ]
    )
    return layout


def update_options(match_history, start, count):
    options = []
    index = start
    for match in match_history:
        index += 1
        progress = index / count * 100
        gamemode = asyncio.run(get_gamemode(match.match_info.ugc_game_variant.asset_id, match.match_info.ugc_game_variant.version_id)).public_name
        map_name = asyncio.run(get_map(match.match_info.map_variant.asset_id, match.match_info.map_variant.version_id)).public_name
        option = {'label': f"{index}: {gamemode} - {map_name}", 'value': f"{match.match_id}"}
        options.append(option)
        set_props('dropdown-selection', {'options': options})
