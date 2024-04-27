from django import forms
from django.contrib.auth.models import User

from .models import Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'edited_username']
