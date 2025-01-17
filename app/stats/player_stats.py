

def get_core_stats(player)
    for team_stats in player.player_team_stats:
        core_stats = team_stats.stats.core_stats
        player_stats = {
            "categories": ["kills", "deaths", "assists", "damage_dealt", "damage_taken", "accuracy", "shots_hit", "shots_fired"],
            "raw_values": [core_stats.kills, core_stats.deaths, core_stats.assists, core_stats.damage_dealt, core_stats.damage_taken, core_stats.accuracy, core_stats.shots_hit, core_stats.shots_fired],
            "scaled_values": [
                core_stats.kills / max_kills,
                min_deaths / core_stats.deaths if core_stats !=0 else min_deaths / 1,
                core_stats.assists / max_assists,
                core_stats.damage_dealt / max_damage,
                core_stats.damage_taken / max_damage_taken,
                core_stats.accuracy / max_accuracy,
                core_stats.shots_hit / max_shots_hit,
                core_stats.shots_fired / max_shots_fired
                ]
        }
        return player_stats
        