from django.http import HttpResponse, FileResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def image(request):
    return FileResponse()

