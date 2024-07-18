from django.urls import path

from quiz import views

urlpatterns = [
    #path('', views.index, name='quiz-index'),
    path('', views.home, name='quiz-home'),
    path('users/', views.users, name='quiz-users'),
    path('image/', views.image, name='quiz-image'),
]