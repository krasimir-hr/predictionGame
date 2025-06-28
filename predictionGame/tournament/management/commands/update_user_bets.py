from django.core.management.base import BaseCommand
from predictionGame.tournament.models import Match
from predictionGame.bets.models import Bet
from predictionGame.users.models import User
from collections import defaultdict

class Command(BaseCommand):
      help = "Update Bets models with point per match data and add total to User points"

      def handle(self, *args, **options):

            aggregated_user_stats = defaultdict(lambda: {
                  "wins": 0,
                  "results": 0,
                  "points": 0,
            })


            for match in Match.objects.prefetch_related('bets').all():
                  for bet in match.bets.all():
                        winner = None
                        predicted_winner = None
                        user = bet.user
                        bet_points = 0

                        if bet.team1_score > bet.team2_score:
                              predicted_winner = match.team_1
                        else:
                              predicted_winner = match.team_2

                        if match.team1_score > match.team2_score:
                              winner = match.team_1
                        else:
                              winner = match.team_2

                        if winner == predicted_winner:
                              bet_points += 2
                              aggregated_user_stats[user]["wins"] += 1
                              aggregated_user_stats[user]["points"] += 2
                              if (match.team1_score == bet.team1_score and match.team2_score == bet.team2_score):
                                    bet_points += 1
                                    aggregated_user_stats[user]["results"] += 1
                                    aggregated_user_stats[user]["points"] += 1

                        bet.bet_points = bet_points
                        bet.save()
                        self.stdout.write(self.style.SUCCESS(f"Updated points for {bet}."))
            
            updated = 0
            for user, stats in aggregated_user_stats.items():
                  self.stdout.write((f"Updating stats for {user}."))
                  user.profile.correct_wins = stats["wins"]
                  user.profile.correct_results = stats["results"]
                  user.profile.total_points = stats["points"]
                  user.profile.save()
                  updated += 1

            self.stdout.write(self.style.SUCCESS(f"Updated stats for {updated} users."))
