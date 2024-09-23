from django.db import models
from django.contrib.auth.models import User

from predictionGame.tournament.models import Match, Team


class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team1_score = models.IntegerField()
    team2_score = models.IntegerField()
    bet_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s bet for {self.match} - {self.team1_score} : {self.team2_score}"


class Wildcards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    most_picked_top = models.CharField(max_length=50, null=False, blank=False)
    most_picked_jgl = models.CharField(max_length=50, null=False, blank=False)
    most_picked_mid = models.CharField(max_length=50, null=False, blank=False)
    most_picked_bot = models.CharField(max_length=50, null=False, blank=False)
    most_picked_sup = models.CharField(max_length=50, null=False, blank=False)
    most_banned_champion = models.CharField(max_length=50, null=False, blank=False)
    player_with_most_kills = models.CharField(max_length=50, null=False, blank=False)
    player_with_most_assists = models.CharField(max_length=50, null=False, blank=False)
    player_with_most_deaths = models.CharField(max_length=50, null=False, blank=False)
    tournament_winner = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username}'s wildcards"


