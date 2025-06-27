from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from predictionGame.bets.models import Bet
from predictionGame.tournament.models import Match


@receiver(post_save, sender=Match)
def calc_points_and_gather_wins_and_results(sender, instance, **kwargs):
    match = instance
    bets = match.bets.all()

    if not match.finished:
        return

    if bets:
        for bet in bets:
            if bet is not None:
                user = bet.user
                profile = user.profile

                match_type = 'BO5'
                match_team1_score = match.team1_score
                match_team2_score = match.team2_score
                bet_team1_score = bet.team1_score
                bet_team2_score = bet.team2_score

                if match_type == 'BO1':
                    if bet_team1_score > bet_team2_score:
                        if match_team1_score > match_team2_score:
                            bet.bet_points += 2
                            profile.correct_wins += 1
                    elif bet_team2_score > bet_team1_score:
                        if match_team2_score > match_team1_score:
                            bet.bet_points += 2
                            profile.correct_wins += 1

                elif match_type == 'BO3':
                    if match_team1_score == 2 and bet_team1_score == 2:
                        bet.bet_points += 2
                        profile.correct_wins += 1
                        if match_team2_score == bet_team2_score:
                            bet.bet_points += 1
                            profile.correct_results += 1
                    elif match_team2_score == 2 and bet_team2_score == 2:
                        bet.bet_points += 2
                        profile.correct_wins += 1
                        if match_team1_score == bet_team1_score:
                            bet.bet_points += 1
                            profile.correct_results += 1

                elif match_type == 'BO5':
                    if match_team1_score == 3 and bet_team1_score == 3:
                        bet.bet_points += 2
                        profile.correct_wins += 1
                        if match_team2_score == bet_team2_score:
                            bet.bet_points += 1
                            profile.correct_results += 1
                    elif match_team2_score == 3 and bet_team2_score == 3:
                        bet.bet_points += 2
                        profile.correct_wins += 1
                        if match_team1_score == bet_team1_score:
                            bet.bet_points += 1
                            profile.correct_results += 1

                bet.save()
                profile.save()
