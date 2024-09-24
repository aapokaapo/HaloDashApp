import spnkr_app
from spnkr.tools import TEAM_MAP
from dash import html, dcc
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime


def ms_to_mins_and_secs(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02}"
    

def create_timeline_chart(match_stats):
    film_events = asyncio.run(spnkr_app.get_film(match_stats.match_id))
    teams_kills = {}
    data = []
    for event in film_events:
        if event.event_type == "kill":
            team_id = next(player.last_team_id for player in match_stats.players if f"{player.player_id}" == f"xuid({event.xuid})")
            try:
                teams_kills[team_id] += 1
            except KeyError:
                teams_kills[team_id] = 1
            data.append(
                {
                    'team': TEAM_MAP[team_id],
                    'kill_count': teams_kills[team_id],
                    'time': datetime.datetime.fromtimestamp(event.time_ms / 1000, tz=datetime.timezone.utc),
                    'gamertag': event.gamertag
                }
            )
    df = pd.DataFrame(data=data)
    fig = px.line(df, x='time', y='kill_count', color='team', category_orders={'team': ['Eagle', 'Cobra']})
    fig.update_xaxes(tickformat="%M:%S")
    graph = dcc.Graph(figure=fig)
    return graph


def create_kills_chart(match_stats):
    film_events = asyncio.run(spnkr_app.get_film(match_stats.match_id))
    time_tolerance = 3
    kills = []
    data = {}
    for event in film_events:
        if event.event_type == "kill":
            team_id = next(player.last_team_id for player in match_stats.players if f"{player.player_id}" == f"xuid({event.xuid})")
            killed_player = next(death_event.gamertag for death_event in film_events if ((-time_tolerance + event.time_ms <= death_event.time_ms <= time_tolerance + event.time_ms) and death_event.event_type == 'death'))
            
            kills.append({
                    'killer': event.gamertag,
                    'victim': killed_player,
                    'team': TEAM_MAP[team_id]
            })
    df = pd.DataFrame(data=kills)
    fig = px.bar(df, x='killer', color='victim', category_orders={'team': ['Eagle', 'Cobra']})
    graph = dcc.Graph(figure=fig)
    return graph
