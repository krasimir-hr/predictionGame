from predictionGame.tournament.models import Match
from predictionGame.bets.models import Bet
from predictionGame.tournament.utils import build_match_context

def global_context(request):
    return {
        'logged_in_user': request.user,
    }

def upcoming_matches(request):
    matches = Match.objects.filter(finished=False).order_by("match_timedate")[:5]
    context = [build_match_context(match) for match in matches]

    bets_dict = {}
    if request.user.is_authenticated:
        user_bets = Bet.objects.filter(user=request.user).select_related('match')
        bets_dict = {
            bet.match.match_id: {
                'team1_score': bet.team1_score,
                'team2_score': bet.team2_score,
            }
            for bet in user_bets
        }

    return {
        "upcoming_matches": context,
        "user_bets": bets_dict
    }