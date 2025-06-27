from django.core.management.base import BaseCommand
from predictionGame.tournament.models import Match, Player, Champion
from collections import defaultdict

class Command(BaseCommand):
   help = "Update Player and Champion models with aggregated stats from match JSON data"

   def handle(self, *args, **options):
      aggregated_player_stats = defaultdict(lambda: {
         "games": 0,
         "dmg": 0,
         "cs": 0,
         "kills": 0,
         "deaths": 0,
         "assists": 0,
         "champ": None,
      })

      aggregated_champion_stats = defaultdict(lambda: {
         "top_picks": 0,
         "jgl_picks": 0,
         "mid_picks": 0,
         "bot_picks": 0,
         "sup_picks": 0,
         "bans": 0,
      })

      for match in Match.objects.prefetch_related('games').all():
         for game in match.games.all():
               for bans_json in [game.team_1_bans_json, game.team_2_bans_json]:
                  for champ in bans_json:
                     aggregated_champion_stats[champ]["bans"] += 1
               for team_json in [game.team_1_players_stats_json, game.team_2_players_stats_json]:
                  idx = 0
                  if not team_json:
                     continue
               
                  for player_data in team_json:
                     name = player_data.get("name")
                     stats = player_data.get("stats", {})
                     champ = player_data.get("champion")
                     if idx == 0 or idx == 5:
                           aggregated_champion_stats[champ]["top_picks"] += 1
                           print(f'Updating {champ} as a top laner')
                     elif idx == 1 or idx == 6:
                           aggregated_champion_stats[champ]["jgl_picks"] += 1
                           print(f'Updating {champ} as a jgl laner')
                     elif idx == 2 or idx == 7:
                           aggregated_champion_stats[champ]["mid_picks"] += 1
                           print(f'Updating {champ} as a mid laner')
                     elif idx == 3 or idx == 8:
                           aggregated_champion_stats[champ]["bot_picks"] += 1
                           print(f'Updating {champ} as a bot laner')
                     elif idx == 4 or idx == 9:
                           aggregated_champion_stats[champ]["sup_picks"] += 1
                           print(f'Updating {champ} as a sup laner')
                     
                     idx += 1
                     
                     if not name or not stats:
                           continue
                           
                     try:
                           kills, deaths, assists = map(int, stats.get("kda", "0/0/0").split("/"))
                           aggregated_player_stats[name]["kills"] += kills
                           aggregated_player_stats[name]["deaths"] += deaths
                           aggregated_player_stats[name]["assists"] += assists
                           aggregated_player_stats[name]["dmg"] += int(float(stats.get("dmg", 0)))
                           aggregated_player_stats[name]["cs"] += int(float(stats.get("cs", 0)))
                           aggregated_player_stats[name]["games"] += 1
                     except Exception as e:
                           self.stderr.write(f"Error updating {name}: {e}")

         updated_players = 0
        
         for name, stats in aggregated_player_stats.items():
            self.stdout.write((f"Updating stats for {name}."))
            try:
                  player = Player.objects.get(name=name)
            except Player.DoesNotExist:
                  continue
            player.total_kills = stats["kills"]
            player.total_deaths = stats["deaths"]
            player.total_assists = stats["assists"]
            player.total_dmg = stats["dmg"]
            player.total_cs = stats["cs"]
            player.total_games = stats["games"]
            player.save()
            updated_players += 1

         updated_champs = 0
         for name, stats in aggregated_champion_stats.items():
            self.stdout.write((f"Updating stats for {name}."))
            try:
                  champion = Champion.objects.get(name=name)
            except Champion.DoesNotExist:
                  continue
            champion.top_picks = stats["top_picks"]
            champion.jgl_picks = stats["jgl_picks"]
            champion.mid_picks = stats["mid_picks"]
            champion.bot_picks = stats["bot_picks"]
            champion.sup_picks = stats["sup_picks"]
            champion.bans = stats["bans"]
            champion.save()
            updated_champs += 1

        
      self.stdout.write(self.style.SUCCESS(f"Updated stats for {updated_players} player entries."))
      self.stdout.write(self.style.SUCCESS(f"Updated stats for {updated_champs} champion entries."))
