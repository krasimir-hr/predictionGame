from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import predictionGame.bets.views as views
from predictionGame.main.views import logout_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('predictionGame.main.urls')),
    path('wildcards/', views.WildcardsView.as_view(), name='wildcards'),
    path('users/', include('predictionGame.users.urls')),
    path('tournament/', include('predictionGame.tournament.urls')),
    path('accounts/', include('allauth.urls')),
    path('submit-bet/', views.submit_bet, name='submit_bet'),
    path('submit-wildcard/', views.submit_wildcard, name='submit-wildcard'),
    # path("__reload__/", include("django_browser_reload.urls")),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
