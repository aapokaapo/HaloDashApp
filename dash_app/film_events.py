import spnkr_app
from spnkr.tools import TEAM_MAP
from dash import html, dcc
import asyncio
import pandas as pd
import plotly.express as px


def create_timeline_chart(match_stats):
    film_events = asyncio.run(spnkr_app.get_film(match_stats.match_id))
    teams_kills = {}
    data = []
    for event in film_events:
        if event.event_type == "kill":
            team_id = [player.last_team_id for player in match_stats.players if player.player_id == f"xuid({event.xuid})"][0]
            try:
                teams_kills[team_id] += 1
            except KeyError:
                teams_kills[team_id] = 1
            data.append(
                {
                    'team': TEAM_MAP[team_id],
                    'kill_count': teams_kills[team_id],
                    'time': event.time_ms,
                    'gamertag': event.gamertag
                }
            )
    df = pd.DataFrame(data=data)
    fig = px.line(df, x='time', y='kill_count', color='team',)
    graph = dcc.Graph(figure=fig)
    return graph


def create_kills_chart(match_stats):
    film_events = asyncio.run(spnkr_app.get_film(match_stats.match_id))
    time_tolerance = 3
    kills = {}
    for event in film_events:
        if event.event_type == "kill":
            killed_player = [death_event.gamertag for death_event in film_events if ((-time_tolerance + event.time_ms <= death_event.time_ms <= time_tolerance + event.time_ms) and death_event.event_type == 'death')][0]
            try:
                kills[event.gamertag][killed_player] += 1
            except KeyError:
                try:
                    kills[event.gamertag][killed_player] = 0
                    kills[event.gamertag][killed_player] += 1
                except KeyError:
                    kills[event.gamertag] = {}
                    kills[event.gamertag][killed_player] = 0
                    kills[event.gamertag][killed_player] += 1
    df = pd.DataFrame.from_dict(data=kills, orient='index')
    fig = px.bar(df, title="Kills", labels={"index": "Gamertag", "value": "Kills", "variable": "Victim"})
    graph = dcc.Graph(figure=fig)
    return graph
