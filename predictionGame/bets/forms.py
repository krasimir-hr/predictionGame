from django import forms
from .models import Bet, Wildcards


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['team1_score', 'team2_score']


class WildCardsForm(forms.ModelForm):
    class Meta:
        model = Wildcards
        fields = [
            'most_picked_champion',
            'most_banned_champion',
            'highest_winrate_champion',
            'player_with_most_kills',
            'player_with_most_assists',
            'player_with_most_deaths'
        ]

        def __init__(self):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['most_picked_champion'].label = 'Most picked champion'


