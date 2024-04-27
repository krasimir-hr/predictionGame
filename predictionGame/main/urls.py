from django.contrib import admin
from django.urls import path, include
from predictionGame.main import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
]
