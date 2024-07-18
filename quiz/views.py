from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, 'quiz/home.html')

def users(request):
    context = dict()
    context['admin'] = User.objects.get(pk=1)
    return render(request, 'quiz/users.html', context)

def image(request):
    return FileResponse()

