from django.contrib import admin
from django.urls import path, include
from predictionGame.main import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('scrape/<str:match_id>/', views.scrape_match, name='scrape_match'),
    path('create/', views.CreateMatchView.as_view(), name='create_match'),
]
