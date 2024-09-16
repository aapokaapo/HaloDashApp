from dash import html, dcc
from spnkr_app import *
from spnkr.tools import TEAM_MAP
from . import film_events


def get_team_stats(match_stats):
    stats = []
    fig = film_events.create_kills_chart(match_stats)
    stats.append(html.Div(fig))
    fig2 = film_events.create_timeline_chart(match_stats)
    stats.append(html.Div(fig2))
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
            children=html.Div(get_team_stats(match_stats))
        ),
        html.Div(id='player_stats')
    ])

    return layout
