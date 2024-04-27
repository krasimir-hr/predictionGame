from django.contrib import admin
from .models import Bet, Wildcards


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    pass


@admin.register(Wildcards)
class WildcardsAdmin(admin.ModelAdmin):
    pass

