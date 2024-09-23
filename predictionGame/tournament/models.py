from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

import json


class Team(models.Model):
    name = models.CharField(max_length=20)
    display_name = models.CharField(max_length=50, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Player(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    total_games = models.IntegerField(blank=True, null=True, default=0)
    total_dmg = models.IntegerField(blank=True, null=True, default=0)
    total_cs = models.IntegerField(blank=True, null=True, default=0)
    total_kills = models.IntegerField(blank=True, null=True, default=0)
    total_assists = models.IntegerField(blank=True, null=True, default=0)
    total_deaths = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.name} - Kills: {self.total_kills}, Assists: {self.total_assists}, Deaths: {self.total_deaths}'


class Match(models.Model):
    match_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_1', blank=True, null=True)
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team_2', blank=True, null=True)
    GAME_TYPE_CHOICES = (
        ('BO1', 'Best of 1'),
        ('BO3', 'Best of 3'),
        ('BO5', 'Best of 5'),
    )
    match_type = models.CharField(max_length=3, choices=GAME_TYPE_CHOICES, blank=True, null=True)
    team1_score = models.IntegerField(default=0, blank=True, null=True)
    team2_score = models.IntegerField(default=0, blank=True, null=True)
    match_timedate = models.DateTimeField(default=datetime(2025, 4, 30, 11, 0, 0))
    users_who_submitted = models.ManyToManyField(User, blank=True, related_name="matches_for_user")
    finished = models.BooleanField(default=False)

    team1_odds_betano = models.CharField(max_length=5, blank=True, null=True)
    team2_odds_betano = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.team_1.name} vs {self.team_2.name} ({self.match_type}) on {self.match_timedate.strftime('%b %d')}"

    class Meta:
        verbose_name_plural = "Matches"


class Game(models.Model):
    game_number = models.IntegerField()

    mvp = models.CharField(max_length=255, blank=True, null=True)

    team_1_picks_json = models.JSONField(max_length=255, blank=True, null=True)
    team_2_picks_json = models.JSONField(max_length=255, blank=True, null=True)

    team_1_bans_json = models.JSONField(max_length=255, blank=True, null=True)
    team_2_bans_json = models.JSONField(max_length=255, blank=True, null=True)

    team_1_team_stats_json = models.JSONField(max_length=500, blank=True, null=True)
    team_2_team_stats_json = models.JSONField(max_length=500, blank=True, null=True)

    team_1_players_stats_json = models.JSONField(max_length=3000, blank=True, null=True)
    team_2_players_stats_json = models.JSONField(max_length=3000, blank=True, null=True)

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='games')

    side_imgs = models.JSONField(max_length=500, blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.match} - Game {self.game_number}'


class Champion(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    img = models.URLField(blank=True, null=True)

    ban_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Pick(models.Model):
    champion = models.ForeignKey(to=Champion, on_delete=models.CASCADE, related_name='picks')
    ROLE_CHOICES = (
        ('top', 'Top Lane'),
        ('jgl', 'Jungle'),
        ('mid', 'Mid Lane'),
        ('bot', 'Bot Lane'),
        ('sup', 'Support'),
    )
    role = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.champion} - {self.role}'

    @classmethod
    def get_role_display(cls, role):
        for value, display_name in cls.ROLE_CHOICES:
            if value == role:
                return display_name
            return role