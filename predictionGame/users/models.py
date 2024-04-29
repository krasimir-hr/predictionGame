import os

from django.db import models
from django.contrib.auth.models import User

from predictionGame.bets.models import Bet
from predictionGame.tournament.models import Match


def profile_picture_path(instance, filename):
    username = instance.user.username
    _, ext = os.path.splitext(filename)
    return f'profile-pictures/{username}-profile-pic{ext}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(blank=True, null=True, default='https://i.pinimg.com/564x/c0/c8/17/c0c8178e509b2c6ec222408e527ba861.jpg')
    correct_wins = models.IntegerField(default=0)
    correct_results = models.IntegerField(default=0)
    bonus_points = models.IntegerField(default=0)
    edited_username = models.CharField(max_length=30, default="")

    def total_points(self):
        total_points = self.correct_wins * 2 + self.correct_results + self.bonus_points
        return total_points

    def show_username(self):
        if not self.edited_username:
            return self.user.username
        else:
            return self.edited_username

