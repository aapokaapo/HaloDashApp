from spnkr_app import *
from spnkr.tools import TEAM_MAP
from . import film_events
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_flag_stats(match_stats, users):
    
    max_capture_assists = max([team_stats.stats.capture_the_flag_stats.flag_capture_assists for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_captures = max([team_stats.stats.capture_the_flag_stats.flag_captures for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_returns = max([team_stats.stats.capture_the_flag_stats.flag_returns for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_secures = max([team_stats.stats.capture_the_flag_stats.flag_secures for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    max_steals = max([team_stats.stats.capture_the_flag_stats.flag_steals for team_stats in [player.player_team_stats[0] for player in match_stats.players]])
    
    for player in match_stats.players:
        
        user = next(user for user in users if f"xuid({user.xuid})" == f"{player.player_id}")
        
        for team_stats in player.player_team_stats:
            flag_stats = team_stats.stats.capture_the_flag_stats
            player_stats = {
                "categories": ["flag_capture_assists", "flag_captures", "flag_returns", "flag_secures", "flag_steals"],
                "raw_values": [flag_stats.flag_capture_assists, flag_stats.flag_captures, flag_stats.flag_returns, flag_stats.flag_secures, flag_stats.flag_steals],
                "scaled_values": [
                    flag_stats.flag_capture_assists / max_capture_assists,
                    flag_stats.flag_captures / max_captures,
                    flag_stats.flag_returns / max_returns,
                    flag_stats.flag_secures / max_secures,
                    flag_stats.flag_steals / max_steals
                ]
            }
            
            fig = px.line_polar(title=f"{user.gamertag}", line_close=True, line_shape="spline", range_r=[0, 1.05], theta=player_stats['categories'], r=player_stats['scaled_values'])
            graph = dcc.Graph(figure=fig, config={"staticPlot": True}, style={'height': '50%', 'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto', 'display': 'block'})
    
    