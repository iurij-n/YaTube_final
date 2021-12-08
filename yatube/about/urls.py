from django.urls import path

from . import views

app_name = 'about'

urlpatterns = [
    path('author/',
         views.AboutAuthorView.as_view(extra_context={
             'title': 'Об авторе проекта'}),
         name='author'),
    path('tech/',
         views.AboutTechView.as_view(extra_context={
             'title': 'Технологии'}),
         name='tech'),
]
