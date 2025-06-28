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
from collections import defaultdict

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

        wildcards_picks = Wildcards.objects.select_related('user', 
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
                                                     )
        
        top_picks = []
        jgl_picks = []
        mid_picks = []
        bot_picks = []
        sup_picks = []
        ban_picks = []
        kills_picks = []
        assists_picks = []
        deaths_picks = []
        winner_picks = []

        for wc in wildcards_picks:
            if wc.most_picked_top:
                top_picks.append({"user": wc.user, "champ": wc.most_picked_top})
            if wc.most_picked_jgl:
                jgl_picks.append({"user": wc.user, "champ": wc.most_picked_jgl})
            if wc.most_picked_mid:
                mid_picks.append({"user": wc.user, "champ": wc.most_picked_mid})
            if wc.most_picked_bot:
                bot_picks.append({"user": wc.user, "champ": wc.most_picked_bot})
            if wc.most_picked_sup:
                sup_picks.append({"user": wc.user, "champ": wc.most_picked_sup})
            if wc.most_banned_champion:
                ban_picks.append({"user": wc.user, "champ": wc.most_banned_champion})
            if wc.player_with_most_kills:
                kills_picks.append({"user": wc.user, "player": wc.player_with_most_kills})
            if wc.player_with_most_assists:
                assists_picks.append({"user": wc.user, "player": wc.player_with_most_assists})
            if wc.player_with_most_deaths:
                deaths_picks.append({"user": wc.user, "player": wc.player_with_most_deaths})
            if wc.tournament_winner:
                winner_picks.append({"user": wc.user, "team": wc.tournament_winner})

        top_picks = sorted(top_picks, key=lambda x: x["champ"].top_picks, reverse=True)
        jgl_picks = sorted(jgl_picks, key=lambda x: x["champ"].jgl_picks, reverse=True)
        mid_picks = sorted(mid_picks, key=lambda x: x["champ"].mid_picks, reverse=True)
        bot_picks = sorted(bot_picks, key=lambda x: x["champ"].bot_picks, reverse=True)
        sup_picks = sorted(sup_picks, key=lambda x: x["champ"].sup_picks, reverse=True)
        ban_picks = sorted(ban_picks, key=lambda x: x["champ"].bans, reverse=True)

        kills_picks = sorted(kills_picks, key=lambda x: (x["player"].total_kills or 0), reverse=True)
        assists_picks = sorted(assists_picks, key=lambda x: (x["player"].total_assists or 0), reverse=True)
        deaths_picks = sorted(deaths_picks, key=lambda x: (x["player"].total_deaths or 0), reverse=True)
    
        def group_picks_by_champ(picks, key_field='champ', key_attr='name'):
            grouped = defaultdict(lambda: {'users': [], 'object': None})
            for pick in picks:
                obj = pick[key_field]
                if obj:
                    key = getattr(obj, key_attr)
                    grouped[key]['users'].append(pick['user'])
                    grouped[key]['object'] = obj
            return grouped

        top_picks_grouped = group_picks_by_champ(top_picks)
        top_picks_grouped = dict(top_picks_grouped)

        jgl_picks_grouped = group_picks_by_champ(jgl_picks)
        jgl_picks_grouped = dict(jgl_picks_grouped)
        
        mid_picks_grouped = group_picks_by_champ(mid_picks)
        mid_picks_grouped = dict(mid_picks_grouped)

        bot_picks_grouped = group_picks_by_champ(bot_picks)
        bot_picks_grouped = dict(bot_picks_grouped)

        sup_picks_grouped = group_picks_by_champ(sup_picks)
        sup_picks_grouped = dict(sup_picks_grouped)

        ban_picks_grouped = group_picks_by_champ(ban_picks)
        ban_picks_grouped = dict(ban_picks_grouped)

        kills_picks_grouped = group_picks_by_champ(kills_picks, key_field='player', key_attr='name')
        kills_picks_grouped = dict(kills_picks_grouped)

        assists_picks_grouped = group_picks_by_champ(assists_picks, key_field='player', key_attr='name')
        assists_picks_grouped = dict(assists_picks_grouped)
        
        deaths_picks_grouped = group_picks_by_champ(deaths_picks, key_field='player', key_attr='name')
        deaths_picks_grouped = dict(deaths_picks_grouped)

        winner_picks_grouped = group_picks_by_champ(winner_picks, key_field='team', key_attr='name')
        winner_picks_grouped = dict(winner_picks_grouped)


        wc_picks_context = {
            "top_picks": top_picks_grouped,
            "jgl_picks": jgl_picks_grouped,
            "mid_picks": mid_picks_grouped,
            "bot_picks": bot_picks_grouped,
            "sup_picks": sup_picks_grouped,
            "ban_picks": ban_picks_grouped,
            "kills_picks": kills_picks_grouped,
            "assists_picks": assists_picks_grouped,
            "deaths_picks": deaths_picks_grouped,
            "winner_picks": winner_picks_grouped,
        }

        context['wc_picks'] = wc_picks_context
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
            