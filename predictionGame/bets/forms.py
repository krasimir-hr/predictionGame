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
            'most_picked_top',
            'most_picked_jgl',
            'most_picked_mid',
            'most_picked_bot',
            'most_picked_sup',
            'most_banned_champion',
            'player_with_most_kills',
            'player_with_most_assists',
            'player_with_most_deaths',
            'tournament_winner',
        ]

        def __init__(self):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fields['most_picked_top'].widget = forms.TextInput(
                    attrs={'id': 'most_picked_top', 'autocomplete': 'off'})
                self.fields['most_picked_jgl'].widget = forms.TextInput(
                    attrs={'id': 'most_picked_jgl', 'autocomplete': 'off'})
                self.fields['most_picked_mid'].widget = forms.TextInput(
                    attrs={'id': 'most_picked_mid', 'autocomplete': 'off'})
                self.fields['most_picked_bot'].widget = forms.TextInput(
                    attrs={'id': 'most_picked_bot', 'autocomplete': 'off'})
                self.fields['most_picked_sup'].widget = forms.TextInput(
                    attrs={'id': 'most_picked_sup', 'autocomplete': 'off'})
                self.fields['most_banned_champion'].widget = forms.TextInput(
                    attrs={'id': 'most-banned-champion', 'autocomplete': 'off'})
                self.fields['player_with_most_kills'].widget = forms.TextInput(
                    attrs={'id': 'player-most-kills', 'autocomplete': 'off'})
                self.fields['player_with_most_assists'].widget = forms.TextInput(
                    attrs={'id': 'player-most-assists', 'autocomplete': 'off'})
                self.fields['player_with_most_deaths'].widget = forms.TextInput(
                    attrs={'id': 'player-most-deaths', 'autocomplete': 'off'})
                self.fields['tournament_winner'].widget = forms.TextInput(
                    attrs={'id': 'tournament_winner', 'autocomplete': 'off'})

