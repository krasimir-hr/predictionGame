from django.urls import path
import views

urlpatterns = [
    path('wildcards/', views.WildcardsView.as_view(), name='wildcards'),
]