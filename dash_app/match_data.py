from dash import html, dcc
from spnkr_app import *
from spnkr.tools import TEAM_MAP
from . import film_events
import plotly.express as px
import pandas as pd


def get_team_stats(match_stats):
    stats = []
    for team in match_stats.teams:
        categories = []
        for category in team.stats:
            model = category[1]
            if model:
                category_dict = model.model_dump()
                category_items = []
                for key in category_dict.keys():
                    category_items.append(html.Div(f"{key}: {category_dict[key]}"))
                categories.append(html.Div([html.Div(f"{category[0]}"), html.Div(category_items)]))
        stats.append(html.Div([html.Div(f"{TEAM_MAP[team.team_id]}"), html.Div(categories)]))

    return stats


def create_team_damage_graph(match_stats):
    data = []
    users = asyncio.run(get_users_for_xuids([player.player_id for player in match_stats.players]))
    for player in match_stats.players:
        user = next(user for user in users if f"xuid({user.xuid})" == f"{player.player_id}")
        team_stats = next(stats for stats in player.player_team_stats if stats.team_id == player.last_team_id)
        damage_dealt = team_stats.stats.core_stats.damage_dealt
        data.append({
            'gamertag': user.gamertag,
            'team': TEAM_MAP[player.last_team_id],
            'damage_dealt': damage_dealt
        })
    df = pd.DataFrame(data=data)
    fig = px.bar(df, x='team', y='damage_dealt', color='gamertag', category_orders={'team':['Eagle', 'Cobra']})
    graph = dcc.Graph(figure=fig)
    
    return graph



def set_layout(match_stats):
    map_info = match_stats.match_info.map_variant
    map_data = asyncio.run(get_map(map_info.asset_id, map_info.version_id))

    gamemode = match_stats.match_info.ugc_game_variant
    gamemode = asyncio.run(get_gamemode(gamemode.asset_id, gamemode.version_id))

    layout = html.Div([
        html.H1(f"Match Stats - {match_stats.match_id}", style={'text-align': 'center'}),
        html.Div(
            id='match_info',
            children=html.Div(
                children=[
                    # html.Div(f"Start time: {match_stats.match_info.start_time.strftime("%Y-%m-%d %H:%M:%S")}"),
                    # html.Div(f"End time: {match_stats.match_info.end_time.strftime("%Y-%m-%d %H:%M:%S")}"),
                    html.Div(f"Duration:{match_stats.match_info.duration}"),
                    html.Div(f"Map:{map_data.public_name}"),
                    html.Div(f"Game Variant:{gamemode.public_name}"),
                    html.Div([html.Div("Game Results:"),
                              html.Div([html.Div(f"{TEAM_MAP[team.team_id]}: {team.stats.core_stats.score}") for team in
                                        match_stats.teams])])
                ]
            )
        ),
        html.Div(
            id='team_stats',
            children=[
                html.Div(create_team_damage_graph(match_stats)),
                html.Div(film_events.create_kills_chart(match_stats)),
                html.Div(film_events.create_timeline_chart(match_stats)),
                html.Div(get_team_stats(match_stats)),
            ]
        ),
        html.Div(id='player_stats')
    ])

    return layout
