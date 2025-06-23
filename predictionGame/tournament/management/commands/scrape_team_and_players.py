import time

from django.core.management.base import BaseCommand
from predictionGame.tournament.models import Player, Team
from predictionGame.tournament.scraper.scrapers.liquidpedia_scrapers.tournament_page_scraper import TournamentPageScraper
from predictionGame.tournament.scraper.formatters.team_data_formatter import TournamentDataFormatter

class Command(BaseCommand):
   help = 'Runs the scraper and updates the database'

   def handle(self, *args, **options):
      scrapper = TournamentPageScraper('https://liquipedia.net/leagueoflegends/Mid-Season_Invitational/2025')
      tournament_raw_data = scrapper.fetch_all()
      tournament_formatter = TournamentDataFormatter(tournament_raw_data)
      tournament_data = tournament_formatter.structure_data()

      self.stdout.write(f"{len(tournament_data)} teams found")

      for team_name, team_info in tournament_data.items():
         self.stdout.write(f"Attempting to add {team_name}")
         team, created = Team.objects.get_or_create(
            name=team_info['abbreviation'],
            defaults={
               'display_name': team_name,
               'logo': team_info['logo_url']
            }
         )

         if created:
            self.stdout.write(self.style.SUCCESS(f"Team created: {team}"))
         else:
            self.stdout.write(self.style.WARNING(f"Team already exists: {team}"))
         
         time.sleep(1)

         for player_data in team_info['roster']:
            player_name = player_data['name']
            photo_url = player_data.get('photo_url')
            self.stdout.write(f"Attempting to add {player_name} to {team_name}")
            player, createdp = Player.objects.get_or_create(
               name=player_name,
               team=team,
               defaults={'photo_url': photo_url}
            )

            if createdp:
               self.stdout.write(self.style.SUCCESS(f"Player created: {player}"))
            else:
               self.stdout.write(self.style.WARNING(f"Team already exists: {player}"))

            time.sleep(1)
