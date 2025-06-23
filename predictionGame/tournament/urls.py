from django.urls import path
from .views import MatchDetailView

urlpatterns = [
    path('match/<int:pk>/', MatchDetailView.as_view(), name='match-detail'),
]