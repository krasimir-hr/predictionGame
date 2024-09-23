from django import forms
from .models import Match


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['match_id', 'match_type', 'match_timedate', 'team1_odds_betano', 'team2_odds_betano']