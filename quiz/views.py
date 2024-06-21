import io

from django.shortcuts import render
from django.http import *
from reportlab.pdfgen import canvas
from PIL import Image, ImageFilter, ImageDraw

# Create your views here.
def home(req):
    return HttpResponse('This is quiz home.')

def create(req):
    return HttpResponse('creating a quiz...')

def json(req):
    return JsonResponse({
        'name': 'Jack Daniel',
        'age': 25,
        'gpa': 3.99
    })

def pdf(req):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, 'Django is Monolith')
    p.showPage()
    p.save()
    buffer.seek(0)
    # how to return a pdf with django
    return FileResponse(buffer, as_attachment=True,
                        filename='Yoyoyo.pdf')

def bg(req):
    f = open('italy.jpg', 'rb')
    return FileResponse(f)

def pil(req):
    img = Image.new('RGB', (100,50))
    drawer = ImageDraw.Draw(img)
    drawer.text((10,10), '1145005 Web Dev', fill=(100,250,120))  
    del drawer
    response = HttpResponse(content_type="image/png")  
    img.save(response, 'PNG')  
    return response

def blurbg(req):
    factor = 10
    if req.GET.get('factor'):
        factor = int(req.GET.get('factor'))
    img = Image.open('italy.jpg')
    blurimg = img.filter(ImageFilter.GaussianBlur(factor))
    res = HttpResponse(content_type='image/png')
    blurimg.save(res, 'PNG')
    return res
