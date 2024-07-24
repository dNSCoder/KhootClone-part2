from django.contrib import admin
from quiz.models import *
# Register your models here.
admin.site.register(Member)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
