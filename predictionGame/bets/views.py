from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Wildcards
from predictionGame.tournament.models import Champion, Player, Team
from .forms import WildCardsForm


class WildcardsView(CreateView, LoginRequiredMixin):
    template_name = 'bets/wildcards.html'
    model = Wildcards
    form_class = WildCardsForm
    success_url = reverse_lazy('wildcards')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        users_wildcards = Wildcards.objects.select_related('user').all()
        context['current_user'] = current_user
        context['wildcards'] = users_wildcards

        role_display_names = dict(Pick.ROLE_CHOICES)

        roles = ['top', 'jgl', 'mid', 'bot', 'sup']
        context['role_picks'] = {}

        role_field_map = {
            'top': 'most_picked_top',
            'jgl': 'most_picked_jgl',
            'mid': 'most_picked_mid',
            'bot': 'most_picked_bot',
            'sup': 'most_picked_sup',
        }

        for role in roles:
            selected_champions = users_wildcards.values_list(role_field_map[role], flat=True).distinct()

            picks_for_role = Pick.objects.filter(
                role=role,
                champion__name__in=selected_champions
            ).select_related('champion').values(
                'champion__name'
            ).annotate(
                pick_count=Count('id')  # Count the times this champion was picked
            ).order_by('-pick_count')

            pick_counts = {pick['champion__name']: pick['pick_count'] for pick in picks_for_role}

            user_data = {}

            for wildcard in users_wildcards:
                selected_champion = getattr(wildcard, role_field_map[role])
                if selected_champion not in user_data:
                    user_data[selected_champion] = []
                user_data[selected_champion].append({
                    'username': wildcard.user.profile.edited_username,
                    'avatar_url': wildcard.user.profile.profile_picture
                })

            champions_data = [
                {
                    'champion': champion,
                    'pick_count': pick_counts.get(champion, 0),
                    'users': user_data.get(champion, [])
                }
                for champion in selected_champions
            ]

            champions_data = sorted(champions_data, key=lambda x: x['pick_count'], reverse=True)

            context['role_picks'][role] = {
                'display_name': f'Most picked {role_display_names[role].lower()}',
                'picks': champions_data,
            }

        role_display_names = {
            'kills': 'Most Kills',
            'assists': 'Most Assists',
            'deaths': 'Most Deaths',
        }

        players_user_data = {
            'kills': {},
            'assists': {},
            'deaths': {},
        }

        for wildcard in users_wildcards:
            player_kills = wildcard.player_with_most_kills
            if player_kills not in players_user_data['kills']:
                players_user_data['kills'][player_kills] = []
            players_user_data['kills'][player_kills].append({
                'username': wildcard.user.profile.edited_username,
                'avatar_url': wildcard.user.profile.profile_picture,
            })

            # For assists
            player_assists = wildcard.player_with_most_assists
            if player_assists not in players_user_data['assists']:
                players_user_data['assists'][player_assists] = []
            players_user_data['assists'][player_assists].append({
                'username': wildcard.user.profile.edited_username,
                'avatar_url': wildcard.user.profile.profile_picture,
            })

            # For deaths
            player_deaths = wildcard.player_with_most_deaths
            if player_deaths not in players_user_data['deaths']:
                players_user_data['deaths'][player_deaths] = []
            players_user_data['deaths'][player_deaths].append({
                'username': wildcard.user.profile.edited_username,
                'avatar_url': wildcard.user.profile.profile_picture,
            })

        context['players_user_data'] = players_user_data

        selected_players_for_kills = users_wildcards.values_list('player_with_most_kills', flat=True).distinct()
        selected_players_for_assists = users_wildcards.values_list('player_with_most_assists', flat=True).distinct()
        selected_players_for_deaths = users_wildcards.values_list('player_with_most_deaths', flat=True).distinct()

        context['players_with_most_kills'] = Player.objects.filter(
            name__in=selected_players_for_kills
        ).order_by('-total_kills').values(
            'name', 'display_name', 'total_kills'
        )

        context['players_with_most_assists'] = Player.objects.filter(
            name__in=selected_players_for_assists
        ).order_by('-total_assists').values(
            'name', 'display_name', 'total_assists'
        )

        context['players_with_most_deaths'] = Player.objects.filter(
            name__in=selected_players_for_deaths
        ).order_by('-total_deaths').values(
            'name', 'display_name', 'total_deaths'
        )

        context['ban_user_data'] = {}
        selected_banned_champions = users_wildcards.values_list('most_banned_champion', flat=True).distinct()

        for wildcard in users_wildcards:
            banned_champion = wildcard.most_banned_champion
            print(banned_champion)
            if banned_champion not in context['ban_user_data']:
                context['ban_user_data'][banned_champion] = []
            context['ban_user_data'][banned_champion].append({
                'avatar_url': wildcard.user.profile.profile_picture,
            })

        context['banned_champions'] = Champion.objects.filter(
            name__in=selected_banned_champions).order_by('-ban_count')

        context['tournament_winners_user_data'] = {}
        selected_winners = users_wildcards.values_list('tournament_winner', flat=True).distinct()

        for wildcard in users_wildcards:
            tournament_winner = wildcard.tournament_winner
            if tournament_winner not in context['tournament_winners_user_data']:
                context['tournament_winners_user_data'][tournament_winner] = []
            context['tournament_winners_user_data'][tournament_winner].append({
                'avatar_url': wildcard.user.profile.profile_picture,
            })

        context['tournament_winners'] = Team.objects.filter(
            name__in=selected_winners
        )

        return context


def search_champions(request):
    query = request.GET.get('q', '').lower()
    normalized_query = query.replace("'", "")

    champions = Champion.objects.all()
    results = []

    for champion in champions:
        champion_name_normalized = champion.name.lower().replace("'", "")
        if normalized_query in champion_name_normalized:
            results.append({'name': champion.name})

    return JsonResponse(results, safe=False)


def search_players(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(name__icontains=query).values('name')
    player_list = list(players)
    return JsonResponse(player_list, safe=False)


def search_teams(request):
    query = request.GET.get('q', '')
    teams = Team.objects.filter(name__icontains=query).values('name')
    team_list = list(teams)
    return JsonResponse(team_list, safe=False)