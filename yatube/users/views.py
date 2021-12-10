from django.contrib.auth.views import LogoutView
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:home')
    template_name = 'users/signup.html'


class LogOut(LogoutView):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        cache.clear()
