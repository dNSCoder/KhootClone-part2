#from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from quiz.models import *
from django.contrib.auth.models import User
from django.shortcuts import render

class UserView(View):
    def get(self, request):
        print('UserView.get()', request.POST)
        context = {
            'questions': Question.objects.count(),
            'user_count': User.objects.count(),
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

class UserTemplateView(TemplateView):
    template_name = 'quiz/users.html'

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
