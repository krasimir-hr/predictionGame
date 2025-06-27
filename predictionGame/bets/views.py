from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
import traceback

from .models import Wildcards
from predictionGame.tournament.models import Champion, Player, Team, Match
from predictionGame.bets.models import Bet
from .forms import WildCardsForm

class WildcardsView(TemplateView):
    template_name = 'bets/wildcards.html'
    model = Wildcards
    success_url = reverse_lazy('wildcards')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wildcards = Wildcards.objects.filter(user=self.request.user).select_related(
            'most_picked_top', 'most_picked_jgl', 'most_picked_mid',
            'most_picked_bot', 'most_picked_sup', 'most_banned_champion',
            'player_with_most_kills', 'player_with_most_assists', 'player_with_most_deaths',
            'tournament_winner'
        ).first()

        def safe_obj_data(obj):
            if obj:
                if hasattr(obj, 'icon'):
                    img_url = obj.icon
                elif hasattr(obj, 'photo_url'):
                    img_url = obj.photo_url
                elif hasattr(obj, 'logo'): 
                    img_url = obj.logo
                else:
                    img_url = None

                return {
                    'name': obj.name,
                    'img_url': img_url,
                }
            return None

        if wildcards:
            context['user_wildcards'] = {
                'most_picked_top': safe_obj_data(wildcards.most_picked_top),
                'most_picked_jgl': safe_obj_data(wildcards.most_picked_jgl),
                'most_picked_mid': safe_obj_data(wildcards.most_picked_mid),
                'most_picked_bot': safe_obj_data(wildcards.most_picked_bot),
                'most_picked_sup': safe_obj_data(wildcards.most_picked_sup),
                'most_banned_champion': safe_obj_data(wildcards.most_banned_champion),
                'player_with_most_kills': safe_obj_data(wildcards.player_with_most_kills),
                'player_with_most_assists': safe_obj_data(wildcards.player_with_most_assists),
                'player_with_most_deaths': safe_obj_data(wildcards.player_with_most_deaths),
                'tournament_winner': safe_obj_data(wildcards.tournament_winner),
            }
        else:
            context['user_wildcards'] = {}


        context['champions'] = Champion.objects.all()
        context['players'] = Player.objects.all()
        context['teams'] = Team.objects.all()
        return context



@csrf_exempt
@login_required
def submit_wildcard(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        model = data.get('model')
        type = data.get('type')
        option =  data.get('option')
        user = request.user

        instance = None

        if type == 'champion':
            instance = Champion.objects.get(name=option)
        elif type == 'player':
            instance = Player.objects.get(name=option)
        elif type == 'team':
            instance = Team.objects.get(name=option)
        
        wildcard, created = Wildcards.objects.update_or_create(
            user=user,
            defaults={
                f'{model}': instance,
            }
            
        )
        return JsonResponse({'success': True, 'created': created})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
            

@csrf_exempt
@login_required
def submit_bet(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    try:
        data = json.loads(request.body)
        match_id = data.get('match_id')
        team1_score = int(data.get('team1_score'))
        team2_score = int(data.get('team2_score'))

        if not match_id:
            return JsonResponse({'error': 'Missing match ID'}, status=400)
        
        match = Match.objects.get(match_id=match_id)
        
        bet, created = Bet.objects.update_or_create(
            match=match,
            user=request.user,
            defaults={
                'team1_score': team1_score,
                'team2_score': team2_score,
            }
            
        )
        return JsonResponse({'success': True, 'bet_id': bet.id, 'created': created})
    
    except Match.DoesNotExist:
        return JsonResponse({'error': 'Match not found'}, status=400)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
            