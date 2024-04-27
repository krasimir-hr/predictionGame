from datetime import datetime
import json

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.db.models import ExpressionWrapper, F, IntegerField

from predictionGame.bets.forms import BetForm
from predictionGame.bets.models import Bet
from predictionGame.tournament.models import Match
from predictionGame.users.models import Profile


class HomePageView(TemplateView):
    template_name = 'main/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        users_with_points = User.objects.annotate(
            total_points=ExpressionWrapper(
                F('profile__correct_wins') * 3 + F('profile__correct_results'),
                output_field=IntegerField()
            )
        )

        # Sort users by total points in descending order
        sorted_users = users_with_points.order_by('-total_points', '-profile__correct_results')

        unresolved_matches = Match.objects.filter(match_timedate__gt=timezone.now())
        pending_matches = unresolved_matches.exclude(users_who_submitted=current_user.id)
        predicted_matches = Match.objects.filter(users_who_submitted=current_user.id).order_by('-match_timedate__date')

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
