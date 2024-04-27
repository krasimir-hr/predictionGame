from django.contrib import admin
from .models import Team, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass
