from django import forms
from quiz.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['quote', 'state', 'country', 'picture_url']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
