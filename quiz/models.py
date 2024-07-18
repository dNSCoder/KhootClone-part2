from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

class Question(TimeStampedModel):
    # id  primary key
    text = models.TextField(default='', verbose_name='คำถาม')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'คำถาม'
        verbose_name = 'คำถาม'

class Answer(TimeStampedModel):
    # id  primary key
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(default='', verbose_name='คำตอบ')
    correct = models.BooleanField(default=False)

    def __str__(self):
        x = '/' if self.correct else 'x'
        return f'{x} {self.text}'

    class Meta:
        verbose_name_plural = 'คำตอบ'
        verbose_name = 'คำตอบ'

