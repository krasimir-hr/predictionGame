from bs4 import BeautifulSoup
from django.db.models import F

from predictionGame.tournament.models import Match, Team, Game, Player, Pick, Champion
import requests
import json

BASE_URL = "https://liquipedia.net/leagueoflegends/Match:ID_"


def construct_match_data(match_id):
    url = BASE_URL + str(match_id)
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')

    team_names = scrape_team_names(soup)
    result = scrape_result(soup)
    number_of_games = 0

    team_1_score, team_2_score = 0, 0

    if '–' in result:
        team_1_score, team_2_score = [int(x) for x in result.split('–')]
        number_of_games = sum([int(x) for x in result.split('–')])

    def get_or_create_team(team_name):
        team, created = Team.objects.get_or_create(
            name=team_name,
        )
        return team

    team_1 = get_or_create_team(team_names[0])
    team_2 = get_or_create_team(team_names[1])

    curr_match = Match.objects.filter(match_id=match_id)[0]
    if curr_match.finished and curr_match.match_type == 'BO1':
        number_of_games = 1

    match, created = Match.objects.update_or_create(
        match_id=match_id,
        defaults={
            'team_1': team_1,
            'team_2': team_2,
            'team1_score': team_1_score,
            'team2_score': team_2_score,
        }
    )

    if number_of_games > 0:
        games_data = construct_games_data(soup, number_of_games)
        for i in range(number_of_games):
            game_data = games_data.pop(0)
            game, create = Game.objects.update_or_create(
                game_number=i + 1,
                match=match,
                defaults={
                    'team_1_picks_json': game_data['picks']['team1'],
                    'team_2_picks_json': game_data['picks']['team2'],
                    'team_1_bans_json': game_data['bans']['team1'],
                    'team_2_bans_json': game_data['bans']['team2'],
                    'team_1_team_stats_json': game_data['team_stats']['team1'],
                    'team_2_team_stats_json': game_data['team_stats']['team2'],
                    'team_1_players_stats_json': game_data['player_stats']['team1'],
                    'team_2_players_stats_json': game_data['player_stats']['team2'],
                    'side_imgs': game_data['side_imgs'],
                    'score': game_data['score'],
                    'length': game_data['length'],
                }
            )



def scrape_team_names(soup):
    team_name_divs = soup.findAll("div", attrs={"class": "match-bm-lol-match-header-team-long"})
    team_names = []
    for team in team_name_divs:
        team_name = team.find('a').text
        team_names.append(team_name)
    return team_names


def scrape_result(soup):
    result = soup.find("div", attrs={"class": "match-bm-lol-match-header-result"}).text
    if result == '–':
        return '0–0'
    return result


def construct_games_data(soup, number_of_games):
    team_stats = scrape_team_stats(soup)
    picks_data, bans_data = scrape_picks_bans(soup)
    team_1_players_data, team_2_players_data = construct_player_data(soup, number_of_games)
    side_imgs = scrape_side_imgs(soup)

    score_divs = soup.findAll('div', attrs={'class': 'match-bm-lol-game-summary-score'})
    scores = []
    for div in score_divs:
        scores.append(div.text)

    lengths = []
    length_divs = soup.findAll('div', attrs={'class': 'match-bm-lol-game-summary-length'})
    for div in length_divs:
        lengths.append(div.text)
    games = []

    for i in range(number_of_games):

        game_data = {
            "team_stats": {
                "team1": {},
                "team2": {},
            },
            "picks": {
                "team1": [],
                "team2": [],
            },
            "bans": {
                "team1": [],
                "team2": [],
            },
            "player_stats": {
                "team1": [],
                "team2": [],
            },
            'side_imgs': [],
        }

        while len(game_data["picks"]["team1"]) < 5:
            game_data["picks"]["team1"].append(picks_data.pop(0))
            game_data["bans"]["team1"].append(bans_data.pop(0))

        while len(game_data["picks"]["team2"]) < 5:
            game_data["picks"]["team2"].append(picks_data.pop(0))
            game_data["bans"]["team2"].append(bans_data.pop(0))

        game_data["team_stats"]["team1"]["kda"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["kda"] = team_stats.pop(0)
        game_data["team_stats"]["team1"]["gold"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["gold"] = team_stats.pop(0)
        game_data["team_stats"]["team1"]["towers"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["towers"] = team_stats.pop(0)
        game_data["team_stats"]["team1"]["inhibitors"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["inhibitors"] = team_stats.pop(0)
        game_data["team_stats"]["team1"]["barons"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["barons"] = team_stats.pop(0)
        game_data["team_stats"]["team1"]["drakes"] = team_stats.pop(0)
        game_data["team_stats"]["team2"]["drakes"] = team_stats.pop(0)

        if len(scores) > 0:
            game_data['score'] = scores.pop(0)
        game_data['length'] = lengths.pop(0)

        for idx in range(2):
            game_data['side_imgs'].append(side_imgs.pop(0))

        for idx in range(5):
            game_data['player_stats']['team1'].append(team_1_players_data.pop(0))
            game_data['player_stats']['team2'].append(team_2_players_data.pop(0))
        games.append(game_data)

    return games


def scrape_side_imgs(soup):
    game_summary_imgs = []
    game_summary_img_divs = soup.findAll("div", attrs={"class": "match-bm-lol-game-summary-faction"})
    for div in game_summary_img_divs:
        img = div.find("img")
        img_src = "https://liquipedia.net" + img['src']
        game_summary_imgs.append(img_src)

    return game_summary_imgs


def scrape_team_stats(soup):
    teams_stats = []

    h2h_stat_sections = soup.findAll("div", attrs={"class": "match-bm-lol-h2h-stat"})
    for section in h2h_stat_sections:
        h2h_stat_divs = section.findAll("div")
        teams_stats.append(h2h_stat_divs[0].text)
        teams_stats.append(h2h_stat_divs[2].text)

    return teams_stats


def scrape_picks_bans(soup):
    picked_champs = []
    banned_champs = []

    picks_uls = soup.findAll("ul", attrs={"class": "match-bm-lol-game-veto-overview-pick"})
    for ul in picks_uls:
        picks_lis = ul.findAll("li", attrs={"class": "match-bm-lol-game-veto-overview-item"})
        for li in picks_lis:
            champ_name = li.find("a").get('title')
            picked_champs.append(champ_name)

    bans_uls = soup.findAll("ul", attrs={"class": "match-bm-lol-game-veto-overview-ban"})
    for ul in bans_uls:
        bans_lis = ul.findAll("li", attrs={"class": "match-bm-lol-game-veto-overview-item"})
        for li in bans_lis:
            champ_name = li.find("a").get('title')
            banned_champs.append(champ_name)
            ban = Champion.objects.filter(name=champ_name).update(ban_count=F('ban_count') + 1)

    return picked_champs, banned_champs


def construct_player_data(soup, number_of_games):
    team_1_players = []
    team_2_players = []

    player_names, player_champs = scrape_players_basic_info(soup)
    players_stats = scrape_players_stats(soup)
    player_runes_spells_urls = scrape_runes_and_spells_urls(soup)
    player_item_urls = scrape_items_urls(soup)

    def append_player_to_team(team_players):
        for idx in range(5):
            player_role = ""
            if idx % 5 == 0:
                player_role = "top"
            elif idx % 5 == 1:
                player_role = "jgl"
            elif idx % 5 == 2:
                player_role = "mid"
            elif idx % 5 == 3:
                player_role = "bot"
            elif idx % 5 == 4:
                player_role = "sup"

            current_player = player_names.pop(0)
            current_champion = player_champs.pop(0)
            current_kda = players_stats.pop(0)
            current_cs = players_stats.pop(0)
            current_dmg = players_stats.pop(0)

            current_kills, current_deaths, current_assists = current_kda.split('/')
            current_kills = int(current_kills)
            current_deaths = int(current_deaths)
            current_assists = int(current_assists)
            current_cs = int(current_cs)
            current_dmg = int(current_dmg)

            champion_instance = Champion.objects.filter(name=current_champion).first()

            pick = Pick.objects.create(
                champion=champion_instance,
                role=player_role,
            )

            team_players.append(
                {
                    "player": current_player,
                    "role": player_role,
                    "champion": current_champion,
                    "kda": current_kda,
                    "cs": current_cs,
                    "dmg_dealt": current_dmg,
                    "rune_urls": [player_runes_spells_urls.pop(0) for _ in range(2)],
                    "summoner_spells_urls": [player_runes_spells_urls.pop(0) for _ in range(2)],
                    "items": [player_item_urls.pop(0) for _ in range(6)],
                }
            )

            player = Player.objects.filter(name=current_player).first()
            if player:
                player.total_games += 1
                player.total_cs += current_cs
                player.total_dmg += current_dmg
                player.total_kills += current_kills
                player.total_assists += current_assists
                player.total_deaths += current_deaths
                player.save()

            else:
                player = Player.objects.create(
                    name=current_player,
                    total_games=1,
                    total_cs=current_cs,
                    total_dmg=current_dmg,
                    total_kills=current_kills,
                    total_assists=current_assists,
                    total_deaths=current_deaths,
            )

    for i in range(number_of_games):
        append_player_to_team(team_1_players)
        append_player_to_team(team_2_players)
    return team_1_players, team_2_players


def scrape_players_basic_info(soup):
    player_names = []
    player_champs = []
    player_name_champs_divs = soup.findAll("div", attrs={"class": "match-bm-lol-players-player-name"})
    for div in player_name_champs_divs:
        player_name = div.find("a").text
        player_champ = div.find("i").text
        player_names.append(player_name)
        player_champs.append(player_champ)

    return player_names, player_champs


def scrape_players_stats(soup):
    players_stats = []
    player_stats_divs = soup.findAll("div", attrs={"class": "match-bm-lol-players-player-stat"})
    for div in player_stats_divs:
        player_stat = div.text
        players_stats.append(player_stat)
    return players_stats


def scrape_runes_and_spells_urls(soup):
    player_runes_spells_urls = []
    player_rune_divs = soup.findAll("div", attrs={"class": "match-bm-lol-players-player-loadout-rs"})
    for div in player_rune_divs:
        player_runes_imgs = div.findAll('img')
        for img in player_runes_imgs:
            img_src = "https://liquipedia.net" + img['src']
            player_runes_spells_urls.append(img_src)
    return player_runes_spells_urls


def scrape_items_urls(soup):
    player_item_urls = []
    player_item_divs = soup.findAll("div", attrs={"class": "match-bm-lol-players-player-loadout-item"})
    for div in player_item_divs:
        player_item_imgs = div.findAll('img')
        for img in player_item_imgs:
            img_src = "https://liquipedia.net" + img['src']
            player_item_urls.append(img_src)
    return player_item_urls
