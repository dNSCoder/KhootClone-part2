import io

from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from reportlab.pdfgen import canvas
from PIL import Image, ImageFilter, ImageDraw
from django.contrib.auth.models import User
from quiz.forms import QuestionForm
from quiz.models import *


# Create your views here.
def home(req):
    #return HttpResponse('This is quiz home.')
    return render(req, 'quiz/home.html')

def users(req):
    #if req.method == 'GET':
    context = {
        'questions': Question.objects.count(),
        'user_count': User.objects.count(),
        'object_list': User.objects.all(),
    }
    return render(req, 'quiz/users.html', context)

def create(req):
    if req.method == 'POST':
        form = QuestionForm(req.POST)
        if form.is_valid():
            form.save()
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


def quiz_data(req):
    questions = Question.objects.all()
    questions_data = []
    for question in questions:
        choices = question.choices.all()
        choices_data = [{'id': choice.id , 'text': choice.text} for choice in choices]
        questions_data.append({
            'id': question.id,
            'text': question.text,
            'choices': choices_data
        })
    return JsonResponse(questions_data, safe=False)

def submit_answer(request):
    if request.method == 'POST':
        print("Submit to backend...")
        print("###########################################")
        print(request.POST.get('question_id'))
        print(request.POST.get('choice_id'))
        print(request.user)
        
        question_id = request.POST.get('question_id')
        choice_id = request.POST.get('choice_id')

        if question_id is None or choice_id is None:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    
        question = Question.objects.get(id=question_id)
        choice = Choice.objects.get(id=choice_id)
        
            # ค้นหา Member ที่เชื่อมโยงกับ user ที่ล็อกอิน
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
        
        # บันทึกคำตอบ
        # ค้นหาจำนวนรอบการทำแบบทดสอบของผู้ใช้ที่มีอยู่แล้ว
            # ดึง attempt_id จาก session
        attempt_id = request.session.get('current_attempt_id')
        if not attempt_id:
            return JsonResponse({'error': 'No quiz attempt found. Please start the quiz again.'}, status=400)
    
        # ดึง QuizAttempt จาก attempt_id
        attempt = get_object_or_404(QuizAttempt, id=attempt_id)
        
        Answer.objects.create(
            member=member,
            question=question,
            choice=choice,
            attempt=attempt
        )
    
        return JsonResponse({'status': 'ok'})

def calculate_score(request):
    # ดึงรอบการทำแบบทดสอบล่าสุด (หรือกำหนดรอบที่ต้องการ)
    if request.method == 'POST':
        try:
            member = Member.objects.get(user=request.user)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
        
        attempt = QuizAttempt.objects.filter(member=member).order_by('-created_at').first()
        print("########################################################################")
        print("attempt:", attempt)
        if not attempt:
            return JsonResponse({'error': 'No attempts found'}, status=404)
    
        # ดึงคำตอบทั้งหมดที่เชื่อมโยงกับ QuizAttempt รอบนี้
        answers = Answer.objects.filter(member=member, attempt=attempt)
        print("########################################################################")
        print("answers:", answers)
        # คำนวณจำนวนคำตอบที่ถูกต้อง
        correct_answers = 0
        for answer in answers:
            if answer.choice.correct:  # ตรวจสอบว่าตัวเลือกที่เลือกถูกต้องหรือไม่
                correct_answers += 1
    
        # คำนวณคะแนน (ปรับสูตรตามที่ต้องการ)
        score = correct_answers
    
        # บันทึกคะแนนใน Result เชื่อมกับรอบที่ผู้ใช้ทำ
        Result.objects.create(
            member=member,
            score=score
        )
        # ลบ attempt_id ออกจาก session
        if 'current_attempt_id' in request.session:
            del request.session['current_attempt_id']
        # หลังจากบันทึกผลแล้ว ส่งผู้ใช้ไปยังหน้าผลลัพธ์
        return redirect('quiz-results2')
