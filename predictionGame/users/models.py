from django.db import models
from django.contrib.auth.models import User

from predictionGame.bets.models import Bet
from predictionGame.tournament.models import Match


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default='images/anon-user.webp')
    correct_wins = models.IntegerField(default=0)
    correct_results = models.IntegerField(default=0)
    bonus_points = models.IntegerField(default=0)
    username = models.CharField(max_length=30, default="")

    def total_points(self):
        total_points = self.correct_wins * 3 + self.correct_results + self.bonus_points
        return total_points

