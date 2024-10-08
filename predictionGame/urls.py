from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import predictionGame.bets.views as views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('predictionGame.main.urls')),
    path('wildcards/', views.WildcardsView.as_view(), name='wildcards'),
    path('users/', include('predictionGame.users.urls')),
    path('search-champions/', views.search_champions, name='search_champions'),
    path('search-players/', views.search_players, name='search-players'),
    path('search-teams/', views.search_teams, name='search-teams'),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
