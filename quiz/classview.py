#from django.views import View
# this is  import django view
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from quiz.models import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserMemberForm, QuestionForm
from django.urls import reverse_lazy
from django.template.loader import render_to_string

class UserView(View):
    def get(self, request):
        print('UserView.get()', request.POST)
        context = {
            'questions': Question.objects.count(),
            'user_count': User.objects.count(),
            'object_list_all': User.objects.all(),
            'object_list': User.objects.all(),
        }
        return render(request, 'quiz/users.html', context)

    def post(self, request):
        print('UserView.post()', request.POST)
        context = {
            'questions': Question.objects.count(),
            'user_count': User.objects.count(),
            'object_list': User.objects.all(),
        }
        return render(request, 'quiz/users.html', context)

#template view extended
class UserTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/users.html'
    login_url = 'quiz-user-login'
    def get_context_data(self, **kwargs):
        return {
            'questions': Question.objects.count(),
            'user_count': User.objects.count(),
            'object_list': User.objects.all(),
        }

class TextLearningView(LoginRequiredMixin,TemplateView):
    template_name = 'quiz/typography/text_styling.html'
    login_url = 'quiz-user-login'

class LayoutLearningView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'quiz/page_layout/layout.html')
        else:
            return redirect('quiz-user-login')
        
class AlpineJSLearningView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/alpinejs/alpinejs_learning.html'
    login_url = 'quiz-user-login'

class QuizView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/quiz_day1.html'
    login_url = 'quiz-user-login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all().prefetch_related('choices')  # pull questions and choices together with prefetch_related
        # questions = list(Question.objects.select_related().values('id', 'text', 'choices__id', 'choices__text', 'choices__correct'))
        return context
        # another way
        # # ดึงข้อมูลของ Question ทั้งหมด
        # questions = Question.objects.all()
        
        # # ดึง Choices สำหรับแต่ละ Question แยกกัน
        # question_data = []
        # for question in questions:
        #     choices = Choice.objects.filter(question=question)
        #     question_data.append({
        #         'question': question,
        #         'choices': choices
        #     })

class QuizResultsView(TemplateView):
    template_name = 'quiz/result_day1.html'  # ชื่อของ template ที่ใช้แสดงผลลัพธ์

    def post(self, request, *args, **kwargs):
        correct_answers = 0
        questions = Question.objects.all()

        for question in questions:
            # selected_choice = request.POST.get(f'question-{question.id}')
            # or 
            selected_choice = request.POST.get('question-' + str(question.id))
            print(selected_choice)
            print(question)
            if selected_choice and Choice.objects.filter(id=selected_choice, correct=True).exists():
                correct_answers += 1

        return self.render_to_response({'correct_answers': correct_answers, 'total_questions': questions.count()})


class QuizView2(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/quiz_day2.html'
    login_url = 'quiz-user-login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt_id = self.request.session.get('current_attempt_id')
        try:
            member = Member.objects.get(user = self.request.user)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member does not  exist'}, status=403)
        # if no
        if not attempt_id:
            last_attempt = QuizAttempt.objects.filter(member=member).order_by('-created_at').first()
            
            if last_attempt:
                attempt_number = last_attempt.attempt_number+1 #Next round
            else:
                attempt_number = 1 # First Start
            
            new_attempt = QuizAttempt.objects.create(member=member, attempt_number=attempt_number)
            #save session value
            self.request.session['current_attempt_id'] = new_attempt.id
            attempt_id = new_attempt.id

        attempt = get_object_or_404(QuizAttempt, id=attempt_id)
        context['attempt'] = attempt
        return context
class QuizResultView2(TemplateView):
    template_name = 'quiz/result_day2.html'
    
    def get_context_data(self, **kwargs):
        try:
            member = Member.objects.get(user=self.request.user)
        except Member.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
        context = super().get_context_data(**kwargs)

        # ดึงผลลัพธ์ล่าสุดของผู้ใช้ที่ล็อกอิน
        user_result = Result.objects.filter(member=member).order_by('created_at').last()
        #user_result = Result.objects.filter(member=member).order_by('-created_at').first()
        context['user_result'] = user_result

        # ดึงคำตอบล่าสุดของผู้เล่นคนอื่น (โหลดด้วย HTMX)
        others_latest_result = Result.objects.exclude(member=member).order_by('created_at').reverse()[:10]
        #others_latest_result = Result.objects.exclude(member=member).order_by('-created_at')[:10]
        context['others_latest_result'] = others_latest_result
        try:
            attempt = QuizAttempt.objects.filter(member=member).order_by('created_at').last()
        except QuizAttempt.DoesNotExist:
            attempt = None
        
        context['user_attempt'] = attempt
            

        return context


class UserListView(ListView):
    model = User
    template_name = 'quiz/users.html'
    #object_list = User.objects.all()

    def get_queryset(self):
        return User.objects.order_by('member__country')





class UserDetailView(DetailView):
    model = User
    template_name = 'quiz/user.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print("********************************")
        print(data)
        return data
         # Get the current object ID from the URL

class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'quiz/member_update_form.html'
    fields = [ 'user', 'quote', 'state', 'country' ]
    
    def get_object(self):
        # Get the object with the ID from the URL
        obj = get_object_or_404(self.model, id=(self.kwargs.get('pk')))
        print("Fetched Object ID:", obj.id)
        print("type: ", isinstance(self.model,Member))# Debug print
        return obj

    def form_valid(self, form):
        # Process the form data and redirect
        return super().form_valid(form)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'quiz/user_confirm_delete.html'
    success_url = 'quiz-users'
    
class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'quiz/member_register_form.html'
    success_url = reverse_lazy('quiz-user-login')
    #step 2
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['member_form'] = UserMemberForm(self.request.POST)
        else:
            data['member_form'] = UserMemberForm()
        return data
    def form_valid(self, form):
        context = self.get_context_data()
        member_form = context['member_form']
        if form.is_valid() and member_form.is_valid():
            user = form.save() #save data
            profile = member_form.save(commit=False)
            profile.user = user #place fk in profile
            profile.save() #save to database with all data
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        # if form.is_valid() :
        #     user = form.save()
        #     user.save()
        #     return super().form_valid(form)
        # else:
        #     return self.form_invalid(form)
class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('quiz-user-login')  # Redirect เมื่อสำเร็จ
    template_name = 'quiz/member_register_form_decor.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        print(data)
        # print(UserMemberForm(self.request.POST))
        # recheck user member form
        if 'member_form' not in data:
            data['member_form'] = UserMemberForm(self.request.POST)
        print(data)
        # print(data['member_form'])
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        member_form = context['member_form']
        if form.is_valid() and member_form.is_valid():
            user = form.save() #save data
            profile = member_form.save(commit=False)
            profile.user = user #place fk in profile
            profile.save() #save to database with all data
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class UserLoginView(LoginView):
    redirect_authenticated_user = True #redicret to LOGIN_REDIRECT_URLin setting
    template_name = 'quiz/member_login_form.html'
    success_url = reverse_lazy('quiz-users')
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('quiz-user-login')
        

class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'quiz/questions_list.html'

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'quiz/components/question_detail.html'

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/components/question_form.html'
    success_url = reverse_lazy('questions_list')

    def form_valid(self, form):
        # บันทึกคำถามก่อน
        # form question use for one request text of question
        response = super().form_valid(form)
        question = self.object

        choices_text = self.request.POST.getlist('choices[]')
        correct_choice_index = int(self.request.POST.get('correct_choice'))

        for i in range(len(choices_text)):
            choice_text = choices_text[i]
            
            Choice.objects.create(
            
            question = self.object,
            text = choice_text,
            correct = (i == correct_choice_index)
            #return 1 if equal 
            )
         # check request from htmx
        if 'HX-request' in self.request.headers:
            # return TemplateResponse(self.request, 'quiz/components/question_item.html', {'question': question})
            rendered_question = render_to_string('quiz/components/question_item.html', {'question': question})
            return HttpResponse(rendered_question)

        return response

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'quiz/components/question_form.html'
    success_url = reverse_lazy('questions_list')
    def form_valid(self, form):
        # บันทึกคำถาม
        response = super().form_valid(form)
        question = self.object
        
        choices_text = self.request.POST.getlist('choices[]')
        correct_choice_index = int(self.request.POST.get('correct_choice'))
        
        # อัพเดตตัวเลือก (choices)
        choices = question.choices.all()  # ตัวเลือกทั้งหมดที่เชื่อมกับ question นี้
        for i, choice in enumerate(choices):
            #use enumerate for access choice data and index
            choice.text = choices_text[i]  # อัปเดตข้อความของตัวเลือก
            choice.correct = (i == correct_choice_index)  # ตั้งค่าว่าตัวเลือกนี้เป็นตัวเลือกที่ถูกต้องหรือไม่
            choice.save()  # บันทึกการเปลี่ยนแปลงลงในฐานข้อมูล
        
        if 'HX-request' in self.request.headers:
            # return TemplateResponse(self.request, 'quiz/components/question_item.html', {'question': question})
            rendered_question = render_to_string('quiz/components/question_item.html', {'question': question})
            return HttpResponse(rendered_question)
        # for i in range(len(choices)):
        #     choice = choices[i]
        #     choice.text = self.request.POST.getlist('choices[]')[i]
        #     choice.correct = (i == correct_choice_index)
        #     choice.save()

        return response



class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'quiz/components/question_confirm_delete.html'
    success_url = reverse_lazy('questions_list')

    def delete(self, request, *args, **kwargs):
        # ตรวจสอบคำขอว่าเป็น HTMX หรือไม่
        response = super().delete(request, *args, **kwargs)
        if request.headers.get('HX-Request'):
            # หากเป็นคำขอ HTMX ส่ง JSON กลับเพื่ออัปเดตหน้า
            print("yes HTMX request")
            return JsonResponse({
                'success': True,
                'message': 'คำถามถูกลบเรียบร้อยแล้ว'
            })
        return response












class ChoiceCreateView(CreateView):
    model = Choice
    #fields = ['member', 'text']
    fields = '__all__'

class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = '__all__'

class ChoiceDeleteView(DeleteView):
    model = Choice
