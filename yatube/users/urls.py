from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/',
         views.SignUp.as_view(extra_context={'title': 'Зарегистрироваться'}),
         name='signup'),
    path('logout/',
         views.LogOut.as_view(template_name='users/logged_out.html',
                            extra_context={'title': 'Вы вышли из системы'}),
         name='logout'),
    path('login/',
         LoginView.as_view(template_name='users/login.html',
                           extra_context={'title': 'Войти'}),
         name='login'),
]
