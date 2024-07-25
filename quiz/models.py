from django.db import models
from django.contrib.auth.models import User
import requests

# Create your models here.
class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Member(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quote = models.TextField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=500, default='')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name_plural = 'สมาชิก'
        verbose_name = 'สมาชิก'

class Question(TimeStampedModel):
    # id  primary key
    member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)
    text = models.TextField(default='', verbose_name='คำถาม')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'คำถาม'
        verbose_name = 'คำถาม'


class Choice(TimeStampedModel):
    # id  primary key
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(default='', verbose_name='คำตอบ')
    correct = models.BooleanField(default=False)

    def __str__(self):
        x = '/' if self.correct else 'x'
        return f'{x} {self.text}'

    class Meta:
        verbose_name_plural = 'ตัวเลือก'
        verbose_name = 'ตัวเลือก'

class Answer(TimeStampedModel):
    # id  primary key
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.member} {self.question} {self.choice}'

    class Meta:
        verbose_name_plural = 'คำตอบ'
        verbose_name = 'คำตอบ'

