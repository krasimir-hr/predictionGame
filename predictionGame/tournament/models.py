from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)
    logo = models.URLField()

    def __str__(self):
        return f"{self.name}"


class Match(models.Model):
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_2')
    GAME_TYPE_CHOICES = (
        ('BO1', 'Best of 1'),
        ('BO3', 'Best of 3'),
        ('BO5', 'Best of 5'),
    )
    game_type = models.CharField(max_length=3, choices=GAME_TYPE_CHOICES)
    team1_score = models.IntegerField(default=0, blank=True, null=True)
    team2_score = models.IntegerField(default=0, blank=True, null=True)
    match_timedate = models.DateTimeField(default=datetime(2024, 4, 30, 11, 0, 0))
    users_who_submitted = models.ManyToManyField(User, blank=True, related_name="matches_for_user")

    def __str__(self):
        return f"{self.team_1.name} vs {self.team_2.name} ({self.game_type}) on {self.match_timedate.strftime('%b %d')}"

    class Meta:
        verbose_name_plural = "Matches"
