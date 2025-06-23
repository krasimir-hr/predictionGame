from django.contrib import admin
from .models import Team, Match, Game, Champion, Player, Item, SummonerSpell, Rune
from django.utils.safestring import mark_safe

import json


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ['pretty_team_1_players_stats_json']
    def pretty_team_1_players_stats_json(self, obj):
        return mark_safe('<pre>{}</pre>'.format(json.dumps(obj.team_1_players_stats_json, indent=4)))

@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Rune)
class RuneAdmin(admin.ModelAdmin):
    pass

@admin.register(SummonerSpell)
class SummonerSpellAdmin(admin.ModelAdmin):
    pass


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

