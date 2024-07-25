from django import forms
from quiz.models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
