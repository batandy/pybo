from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

class Question(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject=models.CharField(max_length=200)
    content=RichTextField(blank=True, null=True)
    create_date=models.DateTimeField()
    modify_date=models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    view_count = models.PositiveIntegerField(default=0)
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
