from django.db import models
from django.contrib.auth.models import User

from predictionGame.tournament.models import Match, Team, Champion, Player


class Bet(models.Model):
    bet_id = models.CharField(max_length=255, null=True, blank=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="bets")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    bet_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s bet for {self.match} - {self.team1_score} : {self.team2_score}"


class Wildcards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    most_picked_top = models.ForeignKey(Champion, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_most_picked_top')
    most_picked_jgl = models.ForeignKey(Champion, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_most_picked_jgl')
    most_picked_mid = models.ForeignKey(Champion, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_most_picked_mid')
    most_picked_bot = models.ForeignKey(Champion, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_most_picked_bot')
    most_picked_sup = models.ForeignKey(Champion, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_most_picked_sup')
    most_banned_champion = models.ForeignKey(Champion, on_delete=models.CASCADE,  max_length=50, null=True, blank=True, related_name='wildcards_most_banned_champion')
    player_with_most_kills = models.ForeignKey(Player, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_player_with_most_kills')
    player_with_most_assists = models.ForeignKey(Player, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_player_with_most_assists')
    player_with_most_deaths = models.ForeignKey(Player, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_player_with_most_deaths')
    tournament_winner = models.ForeignKey(Team, on_delete=models.CASCADE, max_length=50, null=True, blank=True, related_name='wildcards_tournament_winner')

    def __str__(self):
        return f"{self.user.username}'s wildcards"


