import time
from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from predictionGame.tournament.models import Match, Team, Game
from predictionGame.tournament.scraper.scrapers.liquidpedia_scrapers.tournament_page_scraper import TournamentPageScraper
from predictionGame.tournament.scraper.scrapers.liquidpedia_scrapers.match_page_scraper import MatchPageScraper
from predictionGame.tournament.scraper.formatters.match_data_formatter import MatchDataFormatter

import traceback
import sys


class Command(BaseCommand):
    help = "Scrape all match data from a Liquipedia tournament page and populate Match models."

    def handle(self, *args, **options):
        base_url = 'https://liquipedia.net/leagueoflegends/Mid-Season_Invitational/2025'

        self.stdout.write(f"Fetching matches from: {base_url}")
        tournament_scraper = TournamentPageScraper(base_url)
        soup = tournament_scraper.fetch_page()
        match_urls = tournament_scraper.extract_match_urls(soup)
        test_urls = ['leagueoflegends/Match:ID_LCK25Sp2W1_0010']

        if not match_urls:
            self.stdout.write(self.style.ERROR("No match URLs found."))
            return

        self.stdout.write(f"Found {len(match_urls)} matches.")

        final_data = None

        for relative_url in test_urls:
            full_url = relative_url
            self.stdout.write(f"\nProcessing match URL: {full_url}")
            try:
                scraper = MatchPageScraper(full_url)
                initial_raw_data = scraper.fetch_initial_data()
                final__raw_data = scraper.fetch_finished_data()

                formatter = MatchDataFormatter(initial_raw_data, final__raw_data)
                initial_data = formatter.structure_initial_data()
                try:
                    final_data = formatter.structure_final_match_data()
                except Exception as e:
                    self.stdout.write(self.style.ERROR("Skipping due to error: {e}"))

                teams = initial_data.get('teams')
                if not teams or len(teams) < 2:
                    self.stdout.write(self.style.ERROR("Could not parse both team names. Skipping."))
                    continue

                team_1_name = teams[0].get('short_name', 'Unknown')
                team_2_name = teams[1].get('short_name', 'Unknown')

                if (not team_1_name or team_1_name.lower() == 'unknown') and (not team_2_name or team_2_name.lower() == 'unknown'):
                    self.stdout.write(self.style.WARNING("Both team names are unknown. Skipping match."))
                    continue

                if not team_1_name or not team_2_name:
                    self.stdout.write(self.style.ERROR("One or both team names missing. Skipping."))
                    continue

                timestamp = int(initial_data['timestamp'])
                match_datetime = datetime.fromtimestamp(timestamp)

                match_id = slugify(f"{team_1_name}-vs-{team_2_name}-{match_datetime.date()}")

                self.stdout.write(self.style.NOTICE(f'Match ID: {match_id}'))

                if not Match.objects.filter(match_id=match_id, initial_data=True).exists():
                    try:
                        team_1 = Team.objects.get(name=team_1_name)
                        team_2 = Team.objects.get(name=team_2_name)
                    except Team.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"One or both teams not found: {team_1_name}, {team_2_name}. Skipping."))
                        continue

                    

                    game_type_map = {1: 'BO1', 2: 'BO3', 3: 'BO3', 4: 'BO5', 5: 'BO5'}
                    match_type = game_type_map.get(initial_data['total_games'], 'BO1')

                    finished = initial_data['status'].lower() == 'finished'
                    

                    match, created = Match.objects.get_or_create(
                        match_id=match_id,
                        defaults={
                            'team_1': team_1,
                            'team_2': team_2,
                            'match_type': match_type,
                            'match_timedate': match_datetime,
                            'finished': finished,
                            'initial_data': True,
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Match created: {match}"))

                    time.sleep(1)

                else:
                    finished = initial_data['status'].lower() == 'finished'
                    self.stdout.write(self.style.WARNING(f'Match already exists.'))
                    match = Match.objects.get(match_id=match_id)
                    
                    if finished and not match.finished:
                        if final_data is None:
                            self.stdout.write(self.style.WARNING(f"Skipping match: no data returned"))
                            continue
                        team1_score = final_data['team_1_score']
                        team2_score = final_data['team_2_score']
                        match.finished = True
                        match.team1_score = team1_score
                        match.team2_score = team2_score
                        match.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated match to finished: {match}. Final result: {team1_score} - {team2_score}"))

                if Match.objects.filter(match_id=match_id, finished_data=True, finished=True).exists():
                    self.stdout.write(self.style.WARNING('Match already finished and updated'))
                
                elif Match.objects.filter(match_id=match_id, finished_data=False, finished=True).exists():
                    curr_match = Match.objects.get(match_id=match_id)

                    self.stdout.write(f'Updating games for {curr_match}')
                    idx = 1

                    if final_data is None:
                        print(f"Failed to process match at {match_id}: final_data is None")
                        return

                    for match_data in final_data['games']:
                        for data in match_data.values():
                            self.stdout.write(f'Updating game {idx}')
                            game_id = slugify(f"{team_1_name}-vs-{team_2_name}-{match_datetime.date()}-game{idx}")
                            team_1_stats_json = data['team_1']['team_stats']
                            team_2_stats_json = data['team_2']['team_stats']
                            team_1_players_stats_json = data['team_1']['player_stats']
                            team_2_players_stats_json = data['team_2']['player_stats']
                            team_1_bans_json = data['team_1']['bans']
                            team_2_bans_json = data['team_2']['bans']
                            team_1_side_selection = data['team_1']['side_selection']
                            team_2_side_selection = data['team_2']['side_selection']
                            length = data['length']
                            result = data['result']

                            matchh, created = Game.objects.get_or_create(
                                game_id=game_id,
                                defaults={
                                    'team_1_team_stats_json': team_1_stats_json,
                                    'team_2_team_stats_json': team_2_stats_json,
                                    'team_1_players_stats_json': team_1_players_stats_json,
                                    'team_2_players_stats_json': team_2_players_stats_json,
                                    'team_1_bans_json': team_1_bans_json,
                                    'team_2_bans_json': team_2_bans_json,
                                    'length': length,
                                    'result': result,
                                    'team_1_side_selection': team_1_side_selection,
                                    'team_2_side_selection': team_2_side_selection,
                                    'match': curr_match,
                                    'game_number': idx,
                                }
                            )

                            if created:
                                self.stdout.write(self.style.SUCCESS(f"Game {idx} added to {curr_match}"))

                            idx += 1
                    
                    match.finished_data = True
                    team1_score = final_data['team_1_score']
                    team2_score = final_data['team_2_score']

                    print(team1_score, team2_score)
                    match.team1_score = team1_score
                    match.team2_score = team2_score
                    match.save()


            except Exception as e:
                tb = traceback.format_exc()
                self.stdout.write(self.style.ERROR(f"Failed to process match at {full_url}: {str(e)}"))
                self.stdout.write(self.style.ERROR(tb))
