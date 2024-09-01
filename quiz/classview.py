#from django.views import View
# this is  import django view
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from quiz.models import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserMemberForm
from django.urls import reverse_lazy

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
        

## Create Update Delete
class QuestionCreateView(CreateView):
    model = Question
    #fields = ['member', 'text']
    #fields = '__all__'
    fields = ['text']

class ChoiceCreateView(CreateView):
    model = Choice
    #fields = ['member', 'text']
    fields = '__all__'

class ChoiceUpdateView(UpdateView):
    model = Choice
    fields = '__all__'

class ChoiceDeleteView(DeleteView):
    model = Choice
