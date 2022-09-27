from django.contrib import admin
from .models import User
from .models import Question, Category

class QuestionAdmin(admin.ModelAdmin):
    search_fields=['subject']

admin.site.register(Question,QuestionAdmin)
admin.site.register(Category)

# Register your models here.
