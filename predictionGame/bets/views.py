from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Wildcards
from .forms import WildCardsForm


class WildcardsView(CreateView, LoginRequiredMixin):
    template_name = 'bets/wildcards.html'
    model = Wildcards
    form_class = WildCardsForm
    success_url = reverse_lazy('wildcards')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        users_wildcards = Wildcards.objects.all()

        context['current_user'] = current_user
        context['wildcards'] = users_wildcards

        return context
