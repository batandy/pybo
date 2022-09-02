from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)
    has_answer = models.BooleanField(default=True)  # 답변가능 여부

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pybo:index', args=[self.name])

class Question(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject=models.CharField(max_length=200)
    content=RichTextField(null=True, blank=True)
    create_date=models.DateTimeField()
    modify_date=models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    view_count = models.PositiveIntegerField(default=0)
    top_fixed = models.BooleanField(verbose_name='상단고정', default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_question')
    def __str__(self):
        return self.subject
    @property
    def update_counter(self):
        self.view_count=self.view_count+1
        self.save()

class Answer(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    content=models.TextField()
    create_date=models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    create_date = models.DateTimeField()
    modify_date=models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer=models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)

