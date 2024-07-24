from django.urls import path
from quiz.views import *

urlpatterns = [
    path('', home, name='quiz-home'),
    path('users/', users, name='quiz-users'),
    path('create/', create),
    path('json/', json),
    path('pdf/', pdf),
    path('bg/', bg),
    path('blurbg/', blurbg),
]

