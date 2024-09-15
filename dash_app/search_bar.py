from dash import html, dcc, set_props
from spnkr_app import get_map, get_gamemode
import asyncio


def set_layout():
    layout = html.Div(
        [
            dcc.Input(id="search_gamertag", type="text", placeholder="", debounce=True),
            dcc.Dropdown(id='dropdown-selection'),
        ]
    )
    return layout


def update_options(match_history):
    options = []
    for match in match_history:
        gamemode = asyncio.run(get_gamemode(match.match_info.ugc_game_variant.asset_id, match.match_info.ugc_game_variant.version_id)).public_name
        map_name = asyncio.run(get_map(match.match_info.map_variant.asset_id, match.match_info.map_variant.version_id)).public_name
        option = {'label': f"{gamemode} - {map_name}", 'value': f"{match.match_id}"}
        options.append(option)
        set_props('dropdown-selection', {'options': options})
