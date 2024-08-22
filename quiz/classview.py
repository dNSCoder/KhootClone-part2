#from django.views import View
# this is  import django view
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View, TemplateView
from quiz.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
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

class UserListView(ListView):
    model = User
    template_name = 'quiz/users.html'
    #object_list = User.objects.all()

    def get_queryset(self):
        return User.objects.order_by('member__country')


class UserDetailView(DetailView):
    model = User
    template_name = 'quiz/user.html'

class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'quiz/member_update_form.html'
    fields = [ 'user', 'quote', 'state', 'country' ]

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

class UserLoginView(LoginView):
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
