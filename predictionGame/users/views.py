from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from .forms import EditProfileForm
from .models import Profile


class ProfileDetailsView(DetailView, LoginRequiredMixin):
    model = User
    template_name = "users/user-profile.html"
    context_object_name = "user"
    pk_url_kwarg = "pk"


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = EditProfileForm
    context_object_name = "profile"
    template_name = 'users/edit-profile.html'

    def get_object(self, queryset=None):
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile-details', args=[self.request.user.id])