from django.urls import path

from quiz import views

urlpatterns = [
    path('', views.index, name='quiz-index'),
    path('image/', views.image, name='quiz-image'),
]