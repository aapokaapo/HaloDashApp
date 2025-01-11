from dash import html, dcc
from spnkr_app import *
from spnkr.tools import TEAM_MAP
from . import film_events
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_player_stats(match_stats):
    
    users = asyncio.run(get_users_for_xuids([player.player_id for player in match_stats.players]))
    
    teams = {}
    max_kills = max([team_stats.stats.core_stats.kills for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_deaths = max([team_stats.stats.core_stats.deaths for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_assists = max([team_stats.stats.core_stats.assists for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_damage = max([team_stats.stats.core_stats.damage_dealt for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_damage_taken = max([team_stats.stats.core_stats.damage_taken for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_accuracy = max([team_stats.stats.core_stats.accuracy for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_shots_hit = max([team_stats.stats.core_stats.shots_hit for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_shots_fired = max([team_stats.stats.core_stats.shots_fired for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    for player in match_stats.players:
        
        user = next(user for user in users if f"xuid({user.xuid})" == f"{player.player_id}")
        
        for team_stats in player.player_team_stats:
            core_stats = team_stats.stats.core_stats
            player_stats = {
                "categories": ["kills", "deaths", "assists", "damage_dealt", "damage_taken", "accuracy", "shots_hit", "shots_fired"],
                "raw_values": [core_stats.kills, core_stats.deaths, core_stats.assists, core_stats.damage_dealt, core_stats.damage_taken, core_stats.accuracy, core_stats.shots_hit, core_stats.shots_fired],
                "scaled_values": [
                    core_stats.kills / max_kills,
                    1 - core_stats.deaths / max_deaths,
                    core_stats.assists / max_assists,
                    core_stats.damage_dealt / max_damage,
                    core_stats.damage_taken / max_damage_taken,
                    core_stats.accuracy / max_accuracy,
                    core_stats.shots_hit / max_shots_hit,
                    core_stats.shots_fired / max_shots_fired
                    ]
            }
            df = pd.DataFrame(data=[player_stats])
            fig = px.line_polar(df, title=f"{user.gamertag}", line_close=True, line_shape="spline", range_r=[0, 1.05], theta=["kills", "deaths", "assists", "damage_dealt", "damage_taken", "accuracy", "shots_hit", "shots_fired"], r=[
                    core_stats.kills / max_kills,
                    core_stats.deaths / max_deaths,
                    core_stats.assists / max_assists,
                    core_stats.damage_dealt / max_damage,
                    core_stats.damage_taken / max_damage_taken,
                    core_stats.accuracy / max_accuracy,
                    core_stats.shots_hit / max_shots_hit,
                    core_stats.shots_fired / max_shots_fired
                    ])
            
            graph = dcc.Graph(figure=fig, config={"staticPlot": True}, style={'height': '50%', 'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'})
            try:
                teams[team_stats.team_id].append(graph)
            except KeyError:
                teams[team_stats.team_id] = []
                teams[team_stats.team_id].append(graph)
    team_divs = []
    for team in teams:
        team_divs.append(html.Div([html.Div(f"{TEAM_MAP[team]}"), html.Div(teams[team])], style={"width":f"{100/len(teams)-1}%", "float": "left"}))
    
    
    return html.Div(team_divs)
            
            


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
    fig = px.bar(df.sort_values(by=['team', 'gamertag']), x='team', y='damage_dealt', color='gamertag', category_orders={'team':['Eagle', 'Cobra']}, labels={'team': 'Team', 'damage_dealt': 'Damage Dealt', 'gamertag': 'Player'})
    graph = dcc.Graph(figure=fig)
    
    return graph


def create_team_flag_stats_graph(match_stats):
    data = []
    users = asyncio.run(get_users_for_xuids([player.player_id for player in match_stats.players]))
    for player in match_stats.players:
        user = next(user for user in users if f"xuid({user.xuid})" == f"{player.player_id}")
        team_stats = next(stats for stats in player.player_team_stats if stats.team_id == player.last_team_id)
        team_id = player.last_team_id
        flag_stats = team_stats.stats.capture_the_flag_stats
        data.append({
            'gamertag': user.gamertag,
            'team': TEAM_MAP[team_id],
            'flag_capture_assists': flag_stats.flag_capture_assists,
            'flag_captures': flag_stats.flag_captures,
            'flag_grabs': flag_stats.flag_grabs,
            'flag_steals': flag_stats.flag_steals,
            'flag_returns': flag_stats.flag_returns,
            'flag_secures': flag_stats.flag_secures,
            'flag_carriers_killed': flag_stats.flag_carriers_killed,
            'flag_returners_killed': flag_stats.flag_returners_killed
        })
    df = pd.DataFrame(data)
    df.sort_values(by=['team', 'gamertag'], inplace=True)
    fig = px.bar(df, x='gamertag', y=['flag_grabs', 'flag_capture_assists', 'flag_steals', 'flag_returns'], color='gamertag',)
    graph = dcc.Graph(figure=fig)
    return graph
    

def set_layout(match_stats):
    map_info = match_stats.match_info.map_variant
    map_data = asyncio.run(get_map(map_info.asset_id, map_info.version_id))

    gamemode = match_stats.match_info.ugc_game_variant
    gamemode = asyncio.run(get_gamemode(gamemode.asset_id, gamemode.version_id))
    map_thumbnail = map_data.files.prefix + [file for file in map_data.files.file_relative_paths if "thumbnail" in file][0]
    
    layout = html.Div([
        html.H1(f"Match Stats - {match_stats.match_id}", style={'text-align': 'center'}),
        html.Div(html.Div(html.Img(src=f"{map_thumbnail}", style={'width': '90%', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'}))),
        html.Div(
            id='match_info',
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
        ),
        html.Div(
            id='team_stats',
            children=[
                html.Div(create_team_damage_graph(match_stats)),
                html.Div(create_team_flag_stats_graph(match_stats)) if match_stats.players[0].player_team_stats[0].stats.capture_the_flag_stats else None,
                html.Div(film_events.create_kills_chart(match_stats)),
                html.Div(film_events.create_timeline_chart(match_stats)),
                html.Div(create_player_stats(match_stats)),
                html.Div(get_team_stats(match_stats)),
            ]
        )
    ])

    return layout
