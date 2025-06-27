# tournament/utils.py or views.py
def build_match_context(match):
    from .models import Item, SummonerSpell, Champion, Rune

    context = {}
    context['match'] = match
    context['bets'] = match.bets.select_related('user')

    items = {item.name: item.icon for item in Item.objects.all()}
    spells = {spell.name: spell.icon for spell in SummonerSpell.objects.all()}
    champions = {champion.name: champion.icon for champion in Champion.objects.all()}
    runes = {rune.name: rune.icon for rune in Rune.objects.all()}
    role_icons = [
        'https://liquipedia.net/commons/images/2/2e/Lol_role_top_icon_darkmode.svg',
        'https://liquipedia.net/commons/images/7/71/Lol_role_jungle_icon_darkmode.svg',
        'https://liquipedia.net/commons/images/f/f4/Lol_role_middle_icon_darkmode.svg',
        'https://liquipedia.net/commons/images/e/ef/Lol_role_bottom_icon_darkmode.svg',
        'https://liquipedia.net/commons/images/7/71/Lol_role_support_icon_darkmode.svg',
    ]

    players_by_game = {}
    game_stats = []

    

    for game in match.games.all().order_by("game_number"):
        team_1_stat_json = game.team_1_team_stats_json
        team_2_stat_json = game.team_2_team_stats_json

        game_stats.append({
            'game_number': game.game_number,
            'team_1': team_1_stat_json,
            'team_2': team_2_stat_json,
        })

        game_players = []
        for team_json in [game.team_1_players_stats_json, game.team_2_players_stats_json]:
            if not team_json:
                continue
            for player in team_json:
                champ_name = player.get("champion")
                champ_icon = {"name": champ_name, "icon": champions.get(champ_name)} if champ_name else None

                spell_icons = []
                loadouts = player.get("loadouts", {})
                for key in ["summoner1", "summoner2"]:
                    spell_name = loadouts.get(key)
                    if spell_name:
                        icon = spells.get(spell_name)
                        spell_icons.append({"name": spell_name, "icon": icon})

                rune_icons = []
                for key in ["primary", "seconady"]:
                    rune_name = loadouts.get(key)
                    if rune_name:
                        icon = runes.get(rune_name)
                        rune_icons.append({"name": rune_name, "icon": icon})

                item_icons = []
                for item_name in player.get("items", []):
                    icon = items.get(item_name)
                    item_icons.append({"name": item_name, "icon": icon})

                stats_list = []
                player_stats_dict = player.get("stats", {})
                player["dmg"] = f"{float(player_stats_dict.get('dmg', 'N/A')) / 1000:.1f}" if player_stats_dict.get("dmg") else "N/A"
                player["cs"] = player_stats_dict.get("cs", "N/A")
                player["gold"] = player_stats_dict.get("gold", "N/A")

                raw_kda_value = None
                for stat_name, stat_value in player_stats_dict.items():
                    stats_list.append({"name": stat_name, "value": stat_value})
                    if stat_name == "kda":
                        raw_kda_value = stat_value.strip()

                if raw_kda_value:
                    try:
                        kills_str, deaths_str, assists_str = raw_kda_value.split('/')
                        kills = int(kills_str)
                        deaths = int(deaths_str)
                        assists = int(assists_str)
                        player["kda_kills"] = kills_str
                        player["kda_deaths"] = deaths_str
                        player["kda_assists"] = assists_str
                        player["kda_ratio"] = f"{(kills + assists) / deaths:.1f}" if deaths != 0 else str(kills + assists)
                    except Exception:
                        player["kda_kills"] = player["kda_deaths"] = player["kda_assists"] = player["kda_ratio"] = "N/A"
                else:
                    player["kda_kills"] = player["kda_deaths"] = player["kda_assists"] = player["kda_ratio"] = "N/A"

                player["player_stats"] = stats_list
                player["item_icons"] = item_icons
                player["spell_icons"] = spell_icons
                player["rune_icons"] = rune_icons
                player["champion_icon"] = champ_icon
                player["team"] = "Team 1" if team_json == game.team_1_players_stats_json else "Team 2"
                game_players.append(player)

        for i, player_obj in enumerate(game_players):
            player_obj['role_icon'] = role_icons[i % len(role_icons)]

        players_by_game[game.game_number] = {
            "team1": game_players[:5],
            "team2": game_players[5:],
            "team_1_stats": game_stats[-1]["team_1"],
            "team_2_stats": game_stats[-1]["team_2"],
            "team_1_side": game.team_1_side_selection,
        }

    context["players_by_game"] = players_by_game
    return context
