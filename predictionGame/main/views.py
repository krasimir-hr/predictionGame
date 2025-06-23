from datetime import datetime
from collections import defaultdict
import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView
from django.db.models import ExpressionWrapper, F, IntegerField
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from predictionGame.bets.models import Bet
from predictionGame.tournament.models import Match, Champion, Player
from predictionGame.tournament.forms import MatchForm
from predictionGame.bets.forms import BetForm


class HomePageView(TemplateView):
    template_name = 'main/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        users_with_points = User.objects.annotate(
            total_points=ExpressionWrapper(
                F('profile__correct_wins') * 3 + F('profile__correct_results') + F('profile__bonus_points'),
                output_field=IntegerField()
            )
        )

        # Sort users by total points in descending order
        sorted_users = users_with_points.order_by('-total_points', '-profile__correct_results')

        unresolved_matches = Match.objects.filter(match_timedate__gt=timezone.now())
        pending_matches = unresolved_matches.exclude(users_who_submitted=current_user.id)
        predicted_matches = Match.objects.filter(users_who_submitted=current_user.id).order_by('-match_timedate__date')

        for match in predicted_matches:
            for game in match.games.all():
                for side in ['team_1_players_stats_json', 'team_2_players_stats_json']:
                    player_list = getattr(game, side, [])
                    
                    for player in player_list:
                        player_name = player.get("name")
                        try:
                            player_obj = Player.objects.get(name=player_name)
                        except Player.DoesNotExist:
                            player_obj = None
                        player["player_obj"] = player_obj

        matches_by_date = defaultdict(list)
        for match in predicted_matches:
            match_date = match.match_timedate.date()
            matches_by_date[match_date].append(match)

        for match_date in matches_by_date:
            matches_by_date[match_date].sort(key=lambda x: x.match_timedate)
        context['user_predicted_matches_by_date'] = dict(matches_by_date)

        champions = Champion.objects.all()
        champions_dict = {champ.name: champ for champ in champions}

        datetime_from_db = datetime(2024, 4, 30, 0, 0, 0)  # Example datetime value

        matches_ids = predicted_matches.values_list('id', flat=True)
        bets_for_matches = {}
        for match_id in matches_ids:
            bets_for_matches[match_id] = Bet.objects.filter(match_id=match_id)

        context['datetime_from_db'] = datetime_from_db.strftime("%Y-%m-%dT%H:%M:%S")
        context['user_pending_matches'] = pending_matches
        context['user_predicted_matches'] = predicted_matches
        context['bets_for_matches'] = bets_for_matches
        context['users'] = sorted_users
        context['champions'] = champions_dict
        context['form'] = MatchForm()

        return context

    def post(self, request, *args, **kwargs):
        for key, value in request.POST.items():
            if key.startswith('team1_score_'):
                match_id = key.split('_')[-1]
                match = Match.objects.get(id=match_id)
                team2_score = request.POST.get('team2_score_' + match_id)

                # Create Bet object
                Bet.objects.create(
                    match=match,
                    user=request.user,
                    team1_score=value,
                    team2_score=team2_score
                )

                match.users_who_submitted.add(request.user)
        return HttpResponseRedirect('/')


class CreateMatchView(CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'main/create_match.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        match_id = form.cleaned_data['match_id']

        return response
