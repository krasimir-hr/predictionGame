from django.urls import path, include
from django.contrib.auth.views import LogoutView

from predictionGame.users import views

urlpatterns = [
    path('logout', LogoutView.as_view()),
    path('<int:pk>/', include([
        path('', views.ProfileDetailsView.as_view(), name="profile-details"),
        path('edit/', views.EditProfileView.as_view(), name="edit-profile"),
    ]))
]