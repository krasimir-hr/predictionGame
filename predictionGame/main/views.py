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
from predictionGame.tournament.utils import build_match_context
from django.contrib.auth import logout

class HomePageView(TemplateView):
    template_name = 'main/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        finished_matches = Match.objects.filter(finished=True).order_by("-match_timedate")
        upcoming_matches = Match.objects.filter(finished=False).order_by("match_timedate")
        users_ranked = User.objects.select_related('profile').order_by('-profile__total_points')

        if self.request.user.is_authenticated:
            user_bets = Bet.objects.filter(user=self.request.user).select_related('match')
            bets_dict = {
                bet.match.match_id: {
                    'team1_score': bet.team1_score,
                    'team2_score': bet.team2_score,
                }
                for bet in user_bets
            }
            context['user_bets'] = bets_dict
        else:
            user_bets = None

        context["finished_matches"] = [build_match_context(match) for match in finished_matches]
        context["upcoming_matches"] = [build_match_context(match) for match in upcoming_matches]
        context["users_ranked"] = users_ranked

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

def logout_view(request):
    logout(request)
    return redirect('home')

class CreateMatchView(CreateView):
    model = Match
    form_class = MatchForm
    template_name = 'main/create_match.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        match_id = form.cleaned_data['match_id']

        return response
